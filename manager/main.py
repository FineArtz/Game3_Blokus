import time
import logging
import signal
import os
import json

import requests

from conf import LEADER_URL, POLLING_WAIT_TIME, MACHINE_ID

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    signal.signal(signal.SIGHUP, signal.SIG_DFL)

    log_file = 'manager_run.log'

    logger = logging.getLogger("main_logger")
    formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(lineno)s \
        %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    accu_time = 0

    if not os.path.exists('job_args'):
        os.mkdir('job_args')
    while True:
        if (accu_time < POLLING_WAIT_TIME):
            time.sleep(0.1)
            accu_time += 0.1
        else:
            accu_time -= POLLING_WAIT_TIME
            start_time = time.time()
            req = requests.get(LEADER_URL, data = {"machine_id": MACHINE_ID})
            result = req.json()
            if result['status'] == 'Success':
                for each_job in result['job']:
                    job_id = each_job['job_id']
                    with open("job_args/job_" + job_id) as f:
                        json.dump(each_job, f)
                    os.system("py3 judge.py --job_id=%s &" % job_id)

            end_time = time.time()
            accu_time += end_time - start_time





