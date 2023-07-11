# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from schemas.hello import HelloSchema
from connect import security
from tasks import task_crawl_twitter


class HelloWorld(Resource):

    @security.http(
        # login_required=True
    )
    def get(self):
        # debug(request.headers)
        task_crawl_twitter.delay(
            keyword="DWF",
            tweet_params={
                'tweet_date': {
                    'from': 1685318400,
                    'to': 1685404799
                },
                'public_metrics': {
                    'retweet_count': {
                        'from': 1,
                        'to': 100
                    },
                    'reply_count': {
                        'from': 0,
                        'to': 0
                    },
                    'like_count': {
                        'from': 0,
                        'to': 0
                    },
                    'quote_count': {
                        'from': 0,
                        'to': 0
                    },
                    'impression_count': {
                        'from': 0,
                        'to': 0
                    },
                },
                'entities': {
                    'hashtags': ['DWF', 'blockchain']
                }
            },
            account_params={
                'account_excludes': ['DWF1', 'DWF123', 'dwf1', 'dwf123'],
                'account_age_range': {
                    'from': 0,
                    'to': 0
                },
                'public_metrics': {
                    'followers_count': {
                        'from': 10,
                        'to': 10000000000
                    },
                    'following_count': {
                        'from': 10,
                        'to': 10000000000
                    },
                    'tweet_count': {
                        'from': 0,
                        'to': 10000000000
                    },
                    'listed_count': {
                        'from': 0,
                        'to': 10000000000
                    },
                },
                'verified': True
            }
        )

        return {'hello': 'world'}

    @security.http(
        form_data=HelloSchema(),  # form_data
        params=HelloSchema(),  # params
        login_required=True  # user
    )
    def post(self, form_data, params, user):

        return {}
