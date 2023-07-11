# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import traceback

import bson.json_util
import requests
import sentry_sdk
import sys
from time import sleep
from pydash import get
from pymongo import MongoClient


sys.path.append(".")
from lib.logger import debug
from lib import TaskStatus, dt_utcnow
from config import Config
from tasks import task_crawl_twitter

db = MongoClient(Config.MONGO_URI, connect=False)['tc-tools']
AnalyticsLogsModel = db['analytics_logs']

# kw_dict = {}
# for arg in sys.argv[1:]:
#     if '=' in arg:
#         sep = arg.find('=')
#         key, value = arg[:sep], arg[sep + 1:]
#         kw_dict[key] = value

if __name__ == "__main__":
    print("gogo")
    while True:
        _analytic_log_processing = AnalyticsLogsModel.find_one(
            filter={'status': TaskStatus.PROCESSING}
        )

        _analytic_log_pending = AnalyticsLogsModel.find_one(
            filter={'status': TaskStatus.PENDING},
            sort=[('_id', 1)]
        )

        if not _analytic_log_processing and _analytic_log_pending:
            AnalyticsLogsModel.update_one(
                filter={'_id': get(_analytic_log_pending, '_id')},
                update={
                    '$set': {
                        'status': TaskStatus.PROCESSING,
                        'updated_time': dt_utcnow(),
                        'updated_by': 'schedule:analyses'
                    }
                }
            )
            task_crawl_twitter.delay(
                data=bson.json_util.dumps(_analytic_log_pending),
                analytic_log_id=str(get(_analytic_log_pending, '_id'))
            )

            debug(get(_analytic_log_pending, '_id'))

            debug("done")

        sleep(300)  # sleep 5m
