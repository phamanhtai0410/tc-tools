import sys



sys.path.append('.')

import bcrypt
from pymongo.mongo_client import MongoClient
from config import Config
from lib.utils import dt_utcnow

ADMIN_USERNAME = 'admin@gmail.com'
ADMIN_PASSWORD = 'admintools'
ADMIN_ROLES = ['super_admin', 'admin', 'users']
ADMIN_NAME = 'admin'

mdb = MongoClient(Config.MONGO_URI)['tc-tools']

print(mdb)

UserModels = mdb['users']

def main():
    UserModels.update_one({
        'username': ADMIN_USERNAME
    }, {
        '$set': {
            'name': ADMIN_NAME,
            'username': ADMIN_USERNAME,
            'roles': ADMIN_ROLES,
            'password': bcrypt.hashpw(password=ADMIN_PASSWORD.encode('utf8'), salt=bcrypt.gensalt()).decode('utf-8'),
            'created_by': 'scripts',
            'created_time': dt_utcnow(),
        }
    }, upsert=True)

main()