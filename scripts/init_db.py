import sys



sys.path.append('.')

import bcrypt
from pymongo.mongo_client import MongoClient
from config import Config
from lib.utils import dt_utcnow
from lib.enums.vertical import VerticalKeywordGroup

ADMIN_USERNAME = 'admin@gmail.com'
ADMIN_PASSWORD = 'admintools'
ADMIN_ROLES = ['admin', 'users']
ADMIN_NAME = 'admin'

mdb = MongoClient(Config.MONGO_URI)['tc-tools']

print(mdb)

UserModels = mdb['users']
VerticalKeywordGroupModels = mdb['vertical_keyword_group']

def main():
    VerticalKeywordGroupModels.update_one({
        'name': VerticalKeywordGroup.ACCOUNT_PARAMETERS
    }, {
        '$set': {
            'name': VerticalKeywordGroup.ACCOUNT_PARAMETERS,
            'weight': 1,
            'created_time': dt_utcnow(),
            'created_by': 'scripts'
        }
    }, upsert=True)
    
    VerticalKeywordGroupModels.update_one({
        'name': VerticalKeywordGroup.TWEET_PARAMETERS
    }, {
        '$set': {
            'name': VerticalKeywordGroup.TWEET_PARAMETERS,
            'weight': 1,
            'created_time': dt_utcnow(),
            'created_by': 'scripts'
        }
    }, upsert=True)


main()