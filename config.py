# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG")
    PROJECT = "dwf-twitter-tools"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')

    # Authentication
    AUTH_ADDRESS = os.getenv('AUTH_ADDRESS', '')
    AUTH_PRIVATE_KEY = os.getenv('AUTH_PRIVATE_KEY', '')
    TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXP_TIME', default='864000'))

    # Config celery worker
    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    BROKER_USE_SSL = True
    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.task_crawl_twitter': {'queue': 'tc-queue'},
        'worker.task_insert_tweets_filtered': {'queue': 'tc-results-queue'},
        'worker.task_insert_analytics_results': {'queue': 'tc-results-queue'},
        'worker.task_sort_analytics_results': {'queue': 'tc-results-queue'},
    }

    # Redis
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))
    REDLOCK_REDIS = json.loads(os.getenv('REDLOCK_REDIS', '[]'))

    # Blockchain
    BSC_RPC_URI = os.getenv('BSC_RPC_URI')
    CHAIN_ID = int(os.getenv('CHAIN_ID'))

    # Twitter
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    DEFAULT_GLOBAL_SETTING_KEY = 'global_setting_key'

    RATE_QUANTITY = 10
    RATE_POINT = 1
