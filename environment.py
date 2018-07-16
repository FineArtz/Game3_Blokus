
# environment

import sys, os
import argparse
import json
from board import Tiles, Board
from player import Player
import shape

def pprint(thing):
    sys.stdout.write(thing + '\n')
    sys.stdout.flush()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    player = []

    parser.add_argument("--players_allocate", default = "AI_0,AI_0", help = "indicate player type and order")
    parser.add_argument("--extra", help = "extra info")
    args = parser.parse_args()

    if args.players_allocate:
        pa = args.players_allocate.split(',')
        if len(pa) != 2:
            raise ValueError("--player_allocate must have two arguments!")
        for i in range(2):
            if pa[i][0:3] == "AI_":
                lv = int(pa[i][3:])
                player.append(Player(0, i, lv))
            elif pa[i] == "human":
                player.append(Player(0, i, -1))
            else:
                raise ValueError("args of --player_allocate must be 'AI_#' or 'human'!")

    if not args.extra is None:
        pass

    """
        '''
            -s x: the player #x will go first
            default x = 0
        '''
        sente = 0
        if '-s' in sys.argv[1:]:
            argpos = sys.argv.index('-s')
            sente = int(sys.argv[argpos + 1]) % 2

        '''
            -p level: pvc mode. Human player is player #0,
                and 'level' is the level of AI
            or
            -c level1 level2: cvc mode. 
                'level1' and 'level2' are the levels of 
                player #0 and player #1 represently
            default: -c 0 0

            -p and -c can not be set simutaneously, 
            or an exception will be thrown
        '''
        if '-p' in sys.argv[1:]:
            if '-c' in sys.argv[1:]:
                raise Exception("config conflict: [-p, -c]")
            argpos = sys.argv.index('-p')
            pType = int(sys.argv[argpos + 1])
            
            player.append(Player(0, sente, -1))
            player.append(Player(0, sente ^ 1, pType))
        elif '-c' in sys.argv[1:]:
            argpos = sys.argv.index('-c')
            pType = [int(sys.argv[argpos + i]) for i in range(2)]
            player.append(Player(0, sente, pType[0]))
            player.append(Player(0, sente ^ 1, pType[1]))
        else:
            player.append(Player(0, sente, 0))
            player.append(Player(0, sente ^ 1, 0))
    """

    board = Board()
    history = {}
    history['step'] = []

    output = {}
    output["status"] = "Success"
    output["action_player_id"] = 0
    output["state"] = board.board

    pprint(json.dumps(output))
    isOver = False

    while True:
        jsInfo = sys.stdin.readline().rstrip()
        info = json.loads(jsInfo)
        act = info['action']
        isPass = info['is_pass']
        playerOrder = info['action_player_id']

        output = {}
        if isPass:
            if isOver:
                output['status'] = "Over"
                output['result'] = {
                    "record" : json.dumps(history),
                    "score" : [p.score for p in player],
                    "winner_id" : 0 if player[0].score > player[1].score else 1
                }
                pprint(json.dumps(output))
                break
            output["status"] = "Success"
            output["action_player_id"] = playerOrder ^ 1
            output["state"] = board.board
            pprint(json.dumps(output))
            isOver = True
            continue

        isOver = False
        tile = []
        tileSize = len(act)
        minx = 14
        miny = 14
        for i in range(tileSize):
            x = act[i]['row']
            y = act[i]['col']
            tile.append([x, y])
            minx = min(minx, x)
            miny = min(miny, y)
        try:
            result = board.dropTile(playerOrder, tile)
        except Exception as e:
            output['status'] = "Error"
            output['reason'] = str(e)
            pprint(json.dumps(output))
            break
        else:
            if result:
                output = {}
                step = {}
                step["player"] = playerOrder
                step["action"] = act
                step["state"] = {}
                history["step"].append(step)

                for i in range(tileSize):
                    tile[i][0] -= minx
                    tile[i][1] -= miny
                tile.sort()
                rotf = 0
                for t in range(21):
                    if shape.tileSizes[t] != tileSize:
                        continue
                    if tile in shape.shapeSet[t]:
                        player[playerOrder].used[t] = True
                        rotf = shape.shapeSet[t].index[tile]
                        break
                player[playerOrder].score += tileSize
                for (i, j) in shape.cornerSet[t][rotf]:
                    if board.isInBound(minx + i, miny + j):
                        if board.board[minx + i][miny + j] == 0:
                            player[playerOrder].corners.update([(minx + i, miny + j)])
                
                output['status'] = "Success"
                output['action_player_id'] = playerOrder ^ 1
                output['state'] = board.board
                pprint(json.dumps(output))

