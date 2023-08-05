import sentry_sdk
from flask import Flask, request
from flask_restful import Api
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_cors import CORS
from flask_cors import cross_origin
from config import Config
from connect import connect_db
app = Flask(__name__)
api = Api(app)
@app.errorhandler(404)
def page_not_found(error):
    return {
               "msg": "The requested URL was not found on the server.",
               "data": {},
               "errors": [],
               "error_code": "E_NOT_FOUND"
           }, 404


@app.errorhandler(500)
def server_error_page(error):
    return {
               "msg": "Internal Server Error",
               "data": {},
               "errors": [],
               "error_code": "E_SERVER"
           }, 500


# Init database
connect_db.init_app(app, Config.MONGO_URI)

@app.before_request
def before_request():
    from services.ip_logger import IpLoggerService
    IpLoggerService.log_new_request()
    

@app.before_first_request
def before_first_request():
    from models import GlobalSettingModel
    _global_setting = GlobalSettingModel.find_one({
        'key': Config.DEFAULT_GLOBAL_SETTING_KEY
    })

    # NOTE: setup default global setting for map
    if not _global_setting:
        GlobalSettingModel.update_one({
            'key': Config.DEFAULT_GLOBAL_SETTING_KEY
        }, {
            'key': Config.DEFAULT_GLOBAL_SETTING_KEY,
            'followers_count': {
                'start': '1',
                'end': '10'
            },
            'following_count': {
                'start': '1',
                'end': '10'
            },
            'tweet_count': {
                'start': '1',
                'end': '10'
            },
            'listed_count': {
                'start': '1',
                'end': '10'
            },
            'account_age_range': {
                'start': '1',
                'end': '10'
            },
            'tweet_date': {
                'start': '1',
                'end': '10'
            },
            'retweet_count': {
                'start': '1',
                'end': '10'
            },
            'reply_count': {
                'start': '1',
                'end': '10'
            },
            'like_count': {
                'start': '1',
                'end': '10'
            },
            'quote_count': {
                'start': '1',
                'end': '10'
            },
            'impression_count': {
                'start': '1',
                'end': '10'
            },
            'account_no_verified_point': 1,
            'account_verified_point': 1,
            'account_business_point': 1,
            'updated_by': 'app'
        }, upsert=True)

# Init sentry
if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        server_name=Config.PROJECT
    )

from resources import api_resources

# Add resource
for prefix, _resource in api_resources.items():
    api.add_resource(_resource, prefix)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5001)
