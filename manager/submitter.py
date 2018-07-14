import time
import requests
import os
import json
import re
import logging
import shutil

from conf import LEADER_URL

log_file = 'submitter_run.log'

logger = logging.getLogger("submitter_logger")
formatter = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(lineno)s \
    %(levelname)s - %(message)s ", "%Y-%m-%d %H:%M:%S")
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

if not os.path.exists('res'):
    os.mkdir('res')
if not os.path.exists('res/old'):
    os.mkdir('res/old')

while True:
    files = os.listdir('res')
    for file_ in files:
        if os.path.isfile('res/' + file_) and file_.startswith('job_') and file_.endswith('.json'):
            f = open('res/' + file_)
            job_id = re.search(r'\d+', file_).group(0)
            ret = json.load(f)
            ret['job_id'] = job_id
            
            r = requests.get(LEADER_URL + 'return_job', data = ret)
            status = r.json().get('ret')
            if status == 'Fail':
                logger.error("Get: %s, data is %s, status is %s" % (LEADER_URL + 'return_job', json.dumps(ret), status))
            else:
                logger.info("Get: %s, data is %s, status is %s" % (LEADER_URL + 'return_job', json.dumps(ret), status))
            shutil.move('res/' + file_, 'res/old')

    time.sleep(0.1)