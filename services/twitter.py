from time import sleep

import tweepy
from pydash import get

from lib.logger import debug


class TwitterServices:

    def __init__(
            self,
            bearer_token: str,
            consumer_key: str,
            consumer_secret: str,
            access_token: str,
            access_token_secret: str
    ):
        self.client_app_only = tweepy.Client(
            bearer_token=bearer_token,
            return_type=dict,
            wait_on_rate_limit=True
        )
        self.client_user_context = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            return_type=dict,
            wait_on_rate_limit=True
        )
        pass

    def search_tweet_contain_keyword(self, keyword: str, tweet_fields: list, end_time: str):
        """
            'author_id,created_at,context_annotations,entities,public_metrics'
            :param keyword: str - keyword use to search in tweet.
            :param end_time: str - end_time use to search tweet.
            :param tweet_fields: list - tweet_fields config from api docs.
        """
        try:
            # _query = f'{" OR ".join(keywords)}'

            res = self.client_app_only.search_recent_tweets(
                query=keyword,
                tweet_fields=','.join(tweet_fields),
                end_time=end_time,
                max_results=10
            )
            return get(res, 'data', [])
        except Exception as e:
            debug(f'SEARCH TWEET CONTAIN KEYWORD ERROR --- {e}')
            return []

    def search_user_info(self, user_ids: list, user_fields: list):
        """
            'public_metrics,created_at,description,verified,verified_type'
            :param user_ids: list - user_ids of accounts need to search info.
            :param user_fields: list - user_fields config from api docs.
        """
        if not user_ids:
            return {}
        try:
            res = self.client_app_only.get_users(
                ids=','.join(user_ids),
                user_fields=','.join(user_fields)
            )
            return get(res, 'data', {})
        except Exception as e:
            debug(f'SEARCH USER INFO ERROR --- {e}')
            return {}

    def check_follower_account_in_list(self, user_id: str, accounts: list):
        """
            :param user_id: str - user_id of account need to search follower.
            :param accounts: list - accounts list to check following.
        """
        if not accounts or not user_id:
            return []
        try:
            _next_token = ''
            _follower = []
            _max_loop = 1
            _loop = 1
            while _next_token is not None and _loop <= _max_loop:
                if _next_token:
                    _res = self.client_app_only.get_users_followers(
                        id=user_id,
                        max_results=1000,
                        pagination_token=_next_token
                    )
                else:
                    _res = self.client_app_only.get_users_followers(
                        id=user_id,
                        max_results=1000
                    )

                _data = get(_res, 'data')
                _next_token = get(_res, 'meta.next_token')
                if not _data:
                    return _follower

                for _item in _data:
                    _username = get(_item, 'username')
                    if _username in accounts:
                        _follower.append(_username)

                # sleep(60)  # sleep 1m
                _loop += 1

            return _follower

        except Exception as e:
            debug(f'CHECK FOLLOWER ACCOUNT IN LIST ERROR --- {e}')
            return []
