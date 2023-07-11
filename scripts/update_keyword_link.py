from pymongo import MongoClient

MONGO_URI = 'mongodb://18.140.62.59:27017/tc-tools'
db = MongoClient(MONGO_URI)['tc-tools']
KeywordSearchLinkModel = db['keyword_search_link']

_updated = KeywordSearchLinkModel.update_many(
    filter={'is_used': True},
    update={
        '$set': {
            'is_used': False
        }
    }
)