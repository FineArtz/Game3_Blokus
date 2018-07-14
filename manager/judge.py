import logging
import os
import time
import argparse
import json
import signal
import re
from subprocess import Popen, PIPE, check_output
import subprocess
import select
import fcntl


from conf import MACHINE_ID, GAME_LONGGEST_TIME

class Server():
    def __init__(self, args):
        self.alive = True
        try:
            self.process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            flags = fcntl.fcntl(self.process.stdout, fcntl.F_GETFL)
            fcntl.fcntl(self.process.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        except Exception as e:
            logger.error(e)
            self.alive = False
    
    def send(self, data, tail='\n'):
        self.process.stdin.write((data + tail).encode('utf-8'))
        self.process.stdin.flush()

    def recv(self, t=0.1, timeout=5):
        r = ''
        pr = self.process.stdout
        wait_time = 0
        while True:
            if not select.select([pr], [], [], 0)[0]:
                time.sleep(t)
                wait_time += t
                if wait_time > timeout:
                    error_exit("环境计算错误")
                continue
            r = pr.read()
            if not r:
                time.sleep(0.1)
                continue
            return r.rstrip()
        return r.rstrip()


def error_exit(reason="内部错误"):
    logger.info("========== END JUDGE   ============")
    with open('res/job_%s.json' % job_id, 'w') as f:
        json.dump({"status": "Error", "reason": reason}, f)
    os._exit(0) # the judge will exit directly

def set_timeout(timeout, callback, player=""):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError
 
        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(timeout)
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError as e:
                logger.error(e)
                error_exit("超时:" + player)
        return to_do
    return wrap


def process_env_ret(env_ret, reamin_time=[]):
    status = env_ret['status']
    if status == "Error":
        error_exit(env_ret.get("reason", "内部错误"))
    elif status == "Over" or status == "Success":
        return env_ret
    else:
        error_exit("内部错误")



if __name__ == '__main__':

    log_file = 'judge_run.log'
    logger = logging.getLogger("manager_logger")
    formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(lineno)s \
        %(levelname)s - %(message)s - machine_id: " + str(MACHINE_ID), "%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id")
    args = parser.parse_args()
    job_id = args.job_id
    logger.info("========== START JUDGE job: %s ============" % job_id)


    ret = True


    if not os.path.exists("job_args/job_%s.json" % job_id):
        logger.error("Can't find args of job_" + job_id)
        error_exit()

    f = open("job_args/job_%s.json" % job_id, 'r')
    try:
        job_args = json.load(f)
    except Exception as e:
        logger.error("Can't prase json args of job:%s, e" % job_id)
        ret = False
    finally:
        f.close()

    game_id = job_args['game_id']
    game_env_path = "src/game_%s/environment.py" % game_id
    
    if not os.path.exists(game_env_path):
        logger.error("Can't find env of game_" + game_id)
        ret = False

    time_limits = job_args['time_limit'].split('/')
    step_time_limit = int(time_limits[0]) 
    player_time_limit = int(time_limits[1])
    players_remain_time = []

    players_allocate = job_args["players_allocate"]
    extra = job_args.get("extra", {})
    players = players_allocate.split(',')
    players_num = len(players)
    players_cmd = []

    # TODO config input and search
    for each_player in players:
        if each_player == 'human':
            players_cmd.append(['human'])
            players_remain_time.append(3600)
        elif each_player == 'AI':
            players_cmd.append(["python3", "src/game_%s/player.py" % (game_id), "--input"])
            players_remain_time.append(player_time_limit)
        elif 'f' in each_player:
            config_id = re.search(r'\d+', each_player).group(0)
            print(["python3", "src/game_%s/player.py" % game_id, "--input"])
            players_cmd.append(["python3", "src/game_%s/player.py" % game_id, "--input"]) # "--config", "ai_config/%s" % config_id,
            players_remain_time.append(player_time_limit)
        elif 'AI_' in each_player and each_player[3:].isdigit():
            ai_id = re.search(r'\d+', each_player).group(0)
            players_cmd.append(["python3", "src/game_%s/player_%s.py" % (game_id, ai_id), "--input"])
            players_remain_time.append(player_time_limit)
        else:
            logger.error("Wrong format of players_allocate: %s" % players_allocate)
            ret = False

    if ret is False:
        error_exit()

    # init environment
    total_steps = 1
    players_history = {}
    for i in range(players_num):
        players_history[i] = []
    server = Server(["python3", game_env_path, "--players_allocate", players_allocate, "--extra", json.dumps(extra)])
    if server.alive is False:
        error_exit()

    # start interacton
    env_ret = json.loads(server.recv())
    process_env_ret(env_ret)
    action_player_id = env_ret["action_player_id"]

    step_history = {}
    step_history["action_player_id"] = -1
    step_history["action"] = {}
    step_history["state"] = env_ret["state"]

    players_history[action_player_id].append(step_history)

    while True:

        # send state to ai
        print("at step:%s" % total_steps)
        players_input = json.dumps({"history": players_history[action_player_id]})
        start_time = time.time()
        try:
            logger.info("ai cmds:" + ' '.join(players_cmd[action_player_id] + [players_input]))
            agent_ret = check_output(args=players_cmd[action_player_id] + [players_input], timeout=player_time_limit)
            agent_ret = json.loads(agent_ret.rstrip())
        except subprocess.TimeoutExpired:
            logger.error("player: %s Timeout at round: %d" % (players[action_player_id], total_steps))
            error_exit("玩家: %s 在第%d步中的单步运算超时" % (players[action_player_id], total_steps))

        end_time = time.time()
        used_time = end_time - start_time
        if used_time > players_remain_time[action_player_id]:
            logger.error("player: %s Timeout at round: %d" % (players[action_player_id], total_steps))
            error_exit("玩家: %s 在第%d步时总运算时间超时" % (players[action_player_id], total_steps))
        else:
            players_remain_time[action_player_id] -= used_time

        # get next action
        if agent_ret.get("status", "Success") == "Fail":
            logger.error("player: %s throw Exception as round:%d" % (players[action_player_id], total_steps))
            error_exit("玩家: %s 在第%d回合计算出错" % (players[action_player_id], total_steps))
        
        del agent_ret['status']
        agent_ret['action_player_id'] = action_player_id

        # send next action to env
        logger.info("send to env:" + json.dumps(agent_ret))
        server.send(json.dumps(agent_ret))

        # get next state and next_player_id
        env_ret = json.loads(server.recv())
        process_env_ret(env_ret)
        step_history = {}
        if env_ret.get("status", "Success") == "Over":
            used_time = []
            # collect result and write into file
            for i in range(players_num):
                if players[i] == "human":
                    used_time.append(3600 - players_remain_time[i])
                else:
                    used_time.append(player_time_limit - players_remain_time[i])
                result = env_ret.get("result", {})
                result["time_used"] = used_time
                result["steps"] = total_steps
            with open('res/job_%s.json' % job_id, 'w') as f:
                json.dump({"status": "Success", "result": result}, f)
            logger.info("========== END JUDGE   ============")
            break
        else:
            
            step_history["action_player_id"] = action_player_id

            action_player_id = env_ret["action_player_id"]
            next_state = env_ret["state"]
            step_history["action"] = agent_ret["action"]
            step_history["state"] = next_state
            players_history[action_player_id].append(step_history)
            total_steps += 1

