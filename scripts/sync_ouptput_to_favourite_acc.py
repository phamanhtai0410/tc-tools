import sys



sys.path.append('.')

import bcrypt
import json
from pymongo.mongo_client import MongoClient
import requests
from lib.utils import dt_utcnow
from lib.enums.vertical import VerticalKeywordGroup

from pydash import get

ADMIN_USERNAME = 'admin@gmail.com'
ADMIN_PASSWORD = 'admintools'
ADMIN_ROLES = ['admin', 'users']
ADMIN_NAME = 'admin'

# mdb = MongoClient("mongodb://admin:admin@localhost:27017")['tc-tools']
mdb = MongoClient("mongodb://18.140.62.59:27017")['tc-tools']
print(mdb)

UserModels = mdb['users']
VerticalKeywordGroupModels = mdb['vertical_keyword_group']

def main():
    # Call API get top score
    headers = {
        'Authorization': 'rmNOMmLP4C0PI6DHkyyQ',
        'Content-Type': 'application/json'
    }   
    r = requests.get('https://tc.dwf-labs.com/api/score')
    
    # print(get(get(r.json(), "data"), "items"))
    _items = get(get(r.json(), "data"), "items")
    
    
    
    # VerticalKeywordGroupModels.update_one({
    #     'name': VerticalKeywordGroup.ACCOUNT_PARAMETERS
    # }, {
    #     '$set': {
    #         'name': VerticalKeywordGroup.ACCOUNT_PARAMETERS,
    #         'weight': 1,
    #         'created_time': dt_utcnow(),
    #         'created_by': 'scripts'
    #     }
    # }, upsert=True)
    
    # VerticalKeywordGroupModels.update_one({
    #     'name': VerticalKeywordGroup.TWEET_PARAMETERS
    # }, {
    #     '$set': {
    #         'name': VerticalKeywordGroup.TWEET_PARAMETERS,
    #         'weight': 1,
    #         'created_time': dt_utcnow(),
    #         'created_by': 'scripts'
    #     }
    # }, upsert=True)


main()