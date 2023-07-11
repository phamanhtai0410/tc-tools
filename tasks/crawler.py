# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from datetime import datetime
from time import sleep

import bson.json_util
from bson import ObjectId
from pydash import get

from config import Config
from lib import dt_utcnow, TaskStatus
from lib.enums.twitter import TweetFields, UserFields
from lib.logger import debug
from models import TweetsFilteredModel, AnalyticsResultsModel, AnalyticsLogsModel
from services.twitter import TwitterServices
from worker import worker

twitter_services = TwitterServices(
    bearer_token=Config.TWITTER_BEARER_TOKEN,
    consumer_key=Config.TWITTER_CONSUMER_KEY,
    consumer_secret=Config.TWITTER_CONSUMER_SECRET,
    access_token=Config.TWITTER_ACCESS_TOKEN,
    access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET
)


@worker.task(name='worker.task_crawl_twitter', rate_limit='1000/s')
def task_crawl_twitter(data, analytic_log_id):
    try:
        _analytic_log = bson.json_util.loads(data)
        # debug(f'analytic_log: {_analytic_log}')

        _analytic_log_id = analytic_log_id

        _engagement_weight = get(_analytic_log, 'engagement_weight', 0)

        _recency_weight = get(_analytic_log, 'recency_weight', 0)

        _follower_quality_weight = get(_analytic_log, 'follower_quality_weight', 0)

        _keywords_groups = get(_analytic_log, 'vertical_keywords')
        _keywords_group = get(_keywords_groups, '[0]')
        _keywords = get(_keywords_group, 'keywords', [])
        _keyword_group_name = get(_analytic_log, 'vertical_keywords.name')
        _keyword_group_weight = get(_analytic_log, 'vertical_keyword_groups_weight')

        _end_time = datetime.strftime(get(_analytic_log, 'end_date'), "%Y-%m-%dT%H:%M:%S.%fZ")

        _tweet_date_start = get(_analytic_log, 'tweet_date.start')
        _tweet_date_end = get(_analytic_log, 'tweet_date.end')

        _retweet_count_start = int(get(_analytic_log, 'retweet_count.start', 0))
        _retweet_count_end = int(get(_analytic_log, 'retweet_count.end', 9223372036854775807))

        _reply_count_start = int(get(_analytic_log, 'reply_count.start', 0))
        _reply_count_end = int(get(_analytic_log, 'reply_count.end', 9223372036854775807))

        _like_count_start = int(get(_analytic_log, 'like_count.start', 0))
        _like_count_end = int(get(_analytic_log, 'like_count.end', 9223372036854775807))

        _quote_count_start = int(get(_analytic_log, 'quote_count.start', 0))
        _quote_count_end = int(get(_analytic_log, 'quote_count.end', 9223372036854775807))

        _impression_count_start = int(get(_analytic_log, 'impression_count.start', 0))
        _impression_count_end = int(get(_analytic_log, 'impression_count.end', 9223372036854775807))

        _vertical_hashtags = []
        if get(_analytic_log, 'hashtags'):
            _vertical_hashtags = get(_analytic_log, 'hashtags')
        _vertical_hashtags_point = 1
        if get(_analytic_log, 'hashtags_point'):
            _vertical_hashtags_point = get(_analytic_log, 'hashtags_point')

        _vertical_mentions = []
        if get(_analytic_log, 'mentions'):
            _vertical_mentions = get(_analytic_log, 'mentions')
        _vertical_mentions_point = 1
        if get(_analytic_log, 'mentions_point'):
            _vertical_mentions_point = get(_analytic_log, 'mentions_point')

        _vertical_cashtags = []
        if get(_analytic_log, 'cashtags'):
            _vertical_cashtags = get(_analytic_log, 'cashtags')
        _vertical_cashtags_point = 1
        if get(_analytic_log, 'cashtags_point'):
            _vertical_cashtags_point = get(_analytic_log, 'cashtags_point')

        _vertical_annotations = []
        if get(_analytic_log, 'annotations'):
            _vertical_annotations = get(_analytic_log, 'annotations')
        _vertical_annotations_point = 1
        if get(_analytic_log, 'annotations_point'):
            _vertical_annotations_point = get(_analytic_log, 'annotations_point')

        # Account Parameter
        _account_age_range_start = int(get(_analytic_log, 'account_age_range.start', 0))
        _account_age_range_end = int(get(_analytic_log, 'account_age_range.end', 9223372036854775807))

        _account_excludes = []
        if get(_analytic_log, 'exclude_account', []):
            _account_excludes = get(_analytic_log, 'exclude_account', [])
        _account_analyst = get(_analytic_log, 'follower_group.accounts', [])

        _followers_count_start = int(get(_analytic_log, 'followers_count.start', 0))
        _followers_count_end = int(get(_analytic_log, 'followers_count.end', 9223372036854775807))

        _following_count_start = int(get(_analytic_log, 'following_count.start', 0))
        _following_count_end = int(get(_analytic_log, 'following_count.end', 9223372036854775807))

        _tweet_count_start = int(get(_analytic_log, 'tweet_count.start', 0))
        _tweet_count_end = int(get(_analytic_log, 'tweet_count.end', 9223372036854775807))

        _listed_count_start = int(get(_analytic_log, 'listed_count.start', 0))
        _listed_count_end = int(get(_analytic_log, 'listed_count.end', 9223372036854775807))

        _account_no_verified_point = get(_analytic_log, 'account_no_verified_point', 0)
        _account_verified_point = get(_analytic_log, 'account_verified_point', 0)
        _account_business_point = get(_analytic_log, 'account_business_point', 0)
        _account_verified_weight = get(_analytic_log, 'account_verified_weight', 0)

        _users_filtered = {}
        _keyword_relevance_total_score = 0
        _followers_quality_total_score = 0
        _keyword_relevance_score = 1
        for _keyword in _keywords:
            """
                * Step 1: Search tweets using [full archive] tweet search by keywords to crawl

                - author_id,created_at,context_annotations,entities,public_metrics
                - Returns 100 Tweets from the last SEVEN days that match a search query.
            """
            _tweets = twitter_services.search_tweet_contain_keyword(
                keyword=_keyword,
                tweet_fields=[
                    TweetFields.AuthorId,
                    TweetFields.CreatedAt,
                    # TweetFields.ContextAnnotations,
                    TweetFields.Entities,
                    TweetFields.PublicMetrics
                ],
                end_time=str(_end_time)
            )

            """
                * Step 2: Filter tweets by predefined parameters (refer [Tweet Parameter] sheet)
            """
            _author_ids = []
            _tweets_qualified = {}
            _tweets_qualified_list = []
            for _tweet in _tweets:
                # tweet_id
                _tweet_id = get(_tweet, 'id')
                # tweet date
                _tweet_date = datetime.strptime(get(_tweet, 'created_at'), "%Y-%m-%dT%H:%M:%S.%fZ")
                _tweet_time = int(_tweet_date.timestamp())
                # public metrics
                _retweet_count = get(_tweet, 'public_metrics.retweet_count')
                _reply_count = get(_tweet, 'public_metrics.reply_count')
                _like_count = get(_tweet, 'public_metrics.like_count')
                _quote_count = get(_tweet, 'public_metrics.quote_count')
                _impression_count = get(_tweet, 'public_metrics.impression_count')
                # author_id
                _tweet_author_id = get(_tweet, 'author_id')
                # text
                _tweet_text = get(_tweet, 'text')
                # context_annotations
                # _tweet_context_annotations = get(_tweet, 'context_annotations')
                # entities
                _hashtags = get(_tweet, 'entities.hashtags', [])
                _urls = get(_tweet, 'entities.urls', [])
                _cashtags = get(_tweet, 'entities.cashtags', [])
                _annotations = get(_tweet, 'entities.annotations', [])
                _mentions = get(_tweet, 'entities.mentions', [])

                # tweet_time
                if _tweet_date_start and _tweet_time < int(_tweet_date_start):
                    continue
                if _tweet_date_end and _tweet_time > int(_tweet_date_end):
                    continue

                # public metrics
                # retweet_count
                if _retweet_count < _retweet_count_start or _retweet_count > _retweet_count_end:
                    continue

                # reply_count
                if _reply_count < _reply_count_start or _reply_count > _reply_count_end:
                    continue

                # like_count
                if _like_count < _like_count_start or _like_count > _like_count_end:
                    continue

                # quote_count
                if _quote_count < _quote_count_start or _quote_count > _quote_count_end:
                    continue

                # impression_count
                if _impression_count < _impression_count_start or _impression_count > _impression_count_end:
                    continue

                # entities
                # TODO: urls
                # - hashtags
                _count_match_hashtags = 0
                for _hashtag in _hashtags:
                    if get(_hashtag, 'tag') in _vertical_hashtags:
                        _count_match_hashtags = _count_match_hashtags + 1

                # - mentions
                _count_match_mentions = 0
                for _mention in _mentions:
                    if get(_mention, 'username') in _vertical_mentions:
                        _count_match_mentions = _count_match_mentions + 1

                # - cashtags
                _count_match_cashtags = 0
                for _cashtag in _cashtags:
                    if get(_cashtag, 'tag') in _vertical_cashtags:
                        _count_match_cashtags = _count_match_cashtags + 1

                # - annotations
                _count_match_annotations = 0
                for _annotation in _annotations:
                    if get(_annotation, 'normalized_text') in _vertical_annotations:
                        _count_match_annotations = _count_match_annotations + 1

                if _vertical_hashtags or _vertical_cashtags or _vertical_mentions or _vertical_annotations:
                    if _count_match_hashtags == 0 and _count_match_mentions == 0 \
                            and _count_match_cashtags == 0 and _count_match_annotations == 0:
                        continue

                _tweets_qualified[_tweet_author_id] = {
                    'author_id': _tweet_author_id,
                    'tweet_id': _tweet_id,
                    'tweet_time': _tweet_time,
                    'hashtags_matched': _count_match_hashtags,
                    'mentions_matched': _count_match_mentions,
                    'cashtags_matched': _count_match_cashtags,
                    'annotations_matched': _count_match_annotations,
                    'retweet_count': _retweet_count,
                    'reply_count': _reply_count,
                    'like_count': _like_count,
                    'quote_count': _quote_count,
                    'impression_count': _impression_count,
                }
                _tweets_qualified_list.append(
                    {
                        'analytic_log_id': ObjectId(_analytic_log_id),
                        'author_id': _tweet_author_id,
                        'tweet_id': _tweet_id,
                        'tweet_time': _tweet_time,
                        'hashtags_matched': _count_match_hashtags,
                        'mentions_matched': _count_match_mentions,
                        'cashtags_matched': _count_match_cashtags,
                        'annotations_matched': _count_match_annotations,
                        'retweet_count': _retweet_count,
                        'reply_count': _reply_count,
                        'like_count': _like_count,
                        'quote_count': _quote_count,
                        'impression_count': _impression_count,
                    }
                )
                _author_ids.append(_tweet_author_id)

            task_insert_tweets_filtered.delay(
                data=bson.json_util.dumps(_tweets_qualified_list)
            )

            """
                * Step 3: Get account data using user lookup by supplying the author IDs of the remaining tweets after filtered

                   - public_metrics,created_at,description,verified,verified_type
            """
            _users = twitter_services.search_user_info(
                user_ids=_author_ids,
                user_fields=[
                    UserFields.CreatedAt,
                    UserFields.Description,
                    UserFields.PublicMetrics,
                    UserFields.Verified,
                    UserFields.VerifiedType,
                    UserFields.URL
                ]
            )

            """
                * Step 4: Filter accounts by predefined parameters (refer [Account Parameter] sheet)
            """
            # Filter
            for _user in _users:
                # id
                _user_id = get(_user, 'id')
                # name
                _user_name = get(_user, 'name')
                # username
                _user_username = get(_user, 'username')
                # verified
                _user_verified = get(_user, 'verified')
                # verified_type
                _user_verified_type = get(_user, 'verified_type')
                # url
                _user_url = get(_user, 'url')
                # description
                _user_description = get(_user, 'description')
                # created date
                _user_date = datetime.strptime(get(_user, 'created_at'), "%Y-%m-%dT%H:%M:%S.%fZ")
                _user_time = int(_user_date.timestamp())
                _user['created_at'] = int(_user_date.timestamp())
                # public metrics
                _followers_count = get(_user, 'public_metrics.followers_count')
                _following_count = get(_user, 'public_metrics.following_count')
                _tweet_count = get(_user, 'public_metrics.tweet_count')
                _listed_count = get(_user, 'public_metrics.listed_count')

                # excludes accounts
                if _user_username in _account_excludes:
                    continue

                print("gogogogogoog-1")

                # age range
                if _account_age_range_start and _user_time < _account_age_range_start:
                    continue
                if _account_age_range_end and _user_time > _account_age_range_end:
                    continue

                print("gogogogogoog-2")

                # _keyword_in_description = 0
                # for _vertical_keyword in _keywords:
                #     if _vertical_keyword in _user_description:
                #         _keyword_in_description = _keyword_in_description + 1

                # public metrics
                # follower_count
                if _followers_count < _followers_count_start or _followers_count > _followers_count_end:
                    continue

                print("gogogogogoog-3")

                # following_count
                if _following_count < _following_count_start or _following_count > _following_count_end:
                    continue

                print("gogogogogoog-4")

                # tweet_count
                if _tweet_count < _tweet_count_start or _tweet_count > _tweet_count_end:
                    continue

                print("gogogogogoog-5")

                # listed_count
                if _listed_count < _listed_count_start or _listed_count > _listed_count_end:
                    continue

                print("gogogogogoog-6")
                print(f"id: {_user_id}")

                # Verified
                _verify_bonus = _account_no_verified_point
                if _user_verified:
                    if _user_verified_type == 'blue':
                        _verify_bonus = _account_verified_point
                    if _user_verified_type == 'business':
                        _verify_bonus = _account_business_point

                """
                    * Step 5: Score accounts by predefined parameters (refer [Account Parameter] sheet)
                """
                _user_tweet_info = get(_tweets_qualified, f'{_user_id}')
                if not _user_tweet_info:
                    continue

                _hashtags_matched = get(_user_tweet_info, 'hashtags_matched')
                _mentions_matched = get(_user_tweet_info, 'mentions_matched')
                _cashtags_matched = get(_user_tweet_info, 'cashtags_matched')
                _annotations_matched = get(_user_tweet_info, 'annotations_matched')
                _retweet_count = get(_user_tweet_info, 'retweet_count')
                _reply_count = get(_user_tweet_info, 'reply_count')
                _like_count = get(_user_tweet_info, 'like_count')
                _quote_count = get(_user_tweet_info, 'quote_count')
                _impression_count = get(_user_tweet_info, 'impression_count')

                _hashtags_score = _hashtags_matched * _vertical_hashtags_point
                _mentions_score = _mentions_matched * _vertical_mentions_point
                _cashtags_score = _cashtags_matched * _vertical_cashtags_point
                _annotations_score = _hashtags_matched * _vertical_annotations_point

                _retweet_score = (_retweet_count / Config.RATE_QUANTITY * Config.RATE_POINT)
                _reply_score = (_reply_count / Config.RATE_QUANTITY * Config.RATE_POINT)
                _like_score = (_like_count / Config.RATE_QUANTITY * Config.RATE_POINT)
                _quote_score = (_quote_count / Config.RATE_QUANTITY * Config.RATE_POINT)
                _impression_score = (_impression_count / Config.RATE_QUANTITY * Config.RATE_POINT)

                _followers_score = (_followers_count / Config.RATE_QUANTITY * Config.RATE_POINT)
                _following_score = (_following_count / Config.RATE_QUANTITY * Config.RATE_POINT)
                _tweet_score = (_tweet_count / Config.RATE_QUANTITY * Config.RATE_POINT)
                _listed_score = (_listed_count / Config.RATE_QUANTITY * Config.RATE_POINT)

                _engagement_score = (_retweet_score + _reply_score + _like_score + _quote_score + _impression_score + _followers_score + _following_score + _tweet_score + _listed_score) * _engagement_weight / 100

                _verify_score = _verify_bonus * _account_verified_weight / 100

                _keyword_relevance_total_score += _keyword_relevance_score

                # Check user is exist in list
                if _user_id not in _users_filtered:
                    _follower = twitter_services.check_follower_account_in_list(
                        user_id=_user_id,
                        accounts=_account_analyst
                    )
                    _followers_quality_score = len(_follower)
                    _followers_quality_total_score += _followers_quality_score

                    _users_filtered[_user_id] = {
                        'analytic_log_id': ObjectId(_analytic_log_id),
                        **_user,
                        # 'keyword_in_description': _keyword_in_description,
                        'verify_score': _verify_score,
                        'engagement_score': _engagement_score,
                        'followers_quality_score': _followers_quality_score,    # not normalisation
                        'followers_quality_weight': _follower_quality_weight,
                        'recency_score': 0,
                        'keyword_relevance_score': _keyword_relevance_score,    # not normalisation
                        'keyword_relevance_weight': _keyword_group_weight,
                    }
                    continue

                _users_filtered[_user_id]['keyword_relevance_score'] = _users_filtered[_user_id]['keyword_relevance_score'] + _keyword_relevance_score

            sleep(60)
            print("sleeping")

        task_insert_analytics_results.delay(
            data=bson.json_util.dumps(_users_filtered),
            analytic_log_id=str(_analytic_log_id),
            followers_quality_total_score=_followers_quality_total_score,
            keyword_relevance_total_score=_keyword_relevance_total_score
        )
        return 'DONE - task_crawl_twitter'

    except Exception as e:
        AnalyticsLogsModel.update_one(
            filter={'_id': ObjectId(analytic_log_id)},
            obj={
                'status': TaskStatus.FAIL,
                'runtime_note': str(e),
                'updated_time': dt_utcnow(),
                'updated_by': 'task:task_crawl_twitter'
            }
        )
        debug(f'ERROR - task_crawl_twitter: {e}')
        return 'ERROR - task_crawl_twitter'


@worker.task(name='worker.task_insert_tweets_filtered', rate_limit='1000/s')
def task_insert_tweets_filtered(data):
    try:
        _tweets_filtered = bson.json_util.loads(data)

        for _tweet in _tweets_filtered:
            TweetsFilteredModel.insert_one({
                **_tweet,
                'created_time': dt_utcnow(),
                'created_by': 'task:task_insert_tweets_filtered',
                'updated_time': dt_utcnow(),
                'updated_by': '',
            })

        return 'DONE - task_insert_tweets_filtered'

    except Exception as e:
        debug(f'ERROR - task_insert_tweets_filtered: {e}')
        return 'ERROR - task_insert_tweets_filtered'


@worker.task(name='worker.task_insert_analytics_results', rate_limit='1000/s')
def task_insert_analytics_results(data, analytic_log_id, followers_quality_total_score, keyword_relevance_total_score):
    try:
        _users_filtered = bson.json_util.loads(data)

        for _user_id in _users_filtered:
            _user = AnalyticsResultsModel.find_one({
                'analytic_log_id': ObjectId(analytic_log_id),
                'id': str(_user_id)
            })
            if _user:
                continue

            _data = {
                **_users_filtered[_user_id],
                'created_time': dt_utcnow(),
                'created_by': 'task:task_insert_analytics_results',
                'updated_time': dt_utcnow(),
                'updated_by': '',
            }
            # keyword relevance score
            _keyword_relevance_percent = 0
            if keyword_relevance_total_score != 0:
                _keyword_relevance_percent = _data['keyword_relevance_score'] / keyword_relevance_total_score * 100
            _data['keyword_relevance_score'] = _keyword_relevance_percent * _data['keyword_relevance_weight'] / 100
            del _data['keyword_relevance_weight']

            # followers quality score
            _followers_quality_percent = 0
            if followers_quality_total_score != 0:
                _followers_quality_percent = _data['followers_quality_score'] / followers_quality_total_score * 100
            _data['followers_quality_score'] = _followers_quality_percent * _data['followers_quality_weight'] / 100
            del _data['followers_quality_weight']

            AnalyticsResultsModel.insert_one({
                **_data
            })

        task_sort_analytics_results.delay(analytic_log_id=analytic_log_id)

        return 'DONE - task_insert_analytics_results'

    except Exception as e:
        AnalyticsLogsModel.update_one(
            filter={'_id': ObjectId(analytic_log_id)},
            obj={
                'status': TaskStatus.FAIL,
                'runtime_note': str(e),
                'updated_time': dt_utcnow(),
                'updated_by': 'task:task_insert_analytics_results'
            }
        )
        debug(f'ERROR - task_insert_analytics_results: {e}')
        return 'ERROR - task_insert_analytics_results'


@worker.task(name='worker.task_sort_analytics_results', rate_limit='1000/s')
def task_sort_analytics_results(analytic_log_id):
    try:
        _analytics_results = AnalyticsResultsModel.find(
            filter={'analytic_log_id': ObjectId(analytic_log_id)},
            sort=[('created_at', -1)]
        )
        _analytics_log = AnalyticsLogsModel.find_one(filter={'_id': ObjectId(analytic_log_id)})
        _recency_weight = get(_analytics_log, 'recency_weight', 0)
        _total_results = len(_analytics_results)
        _total_recency_score = _total_results * (_total_results + 1) / 2

        for index, _result in enumerate(_analytics_results):
            # (_total_results - index) / _total_recency_score * 100 * _recency_weight / 100
            _recency_score = (_total_results - index) / _total_recency_score * _recency_weight
            _total_score = get(_result, 'verify_score', 0) + get(_result, 'engagement_score', 0) + get(_result, 'keyword_relevance_score', 0) + get(_result, 'followers_quality_score', 0) + _recency_score
            AnalyticsResultsModel.update_one(
                filter={'_id': get(_result, '_id')},
                obj={
                    'recency_score': _recency_score,
                    'total_score': _total_score,
                    'updated_by': 'task:task_sort_analytics_results'
                }
            )

        AnalyticsLogsModel.update_one(
            filter={'_id': ObjectId(analytic_log_id)},
            obj={
                'status': TaskStatus.DONE,
                'updated_by': 'task:task_sort_analytics_results'
            }
        )

        return 'DONE - task_sort_analytics_results'

    except Exception as e:
        debug(f'ERROR - task_sort_analytics_results: {e}')
        return 'ERROR - task_sort_analytics_results'
