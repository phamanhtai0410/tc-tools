# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import bson
from datetime import datetime

from bson import ObjectId
from pydash import get

from exceptions.analytics import AccountFilteredDetailNotExistedEx
from exceptions.request import NotValidObjectIdEx
from helper.format import FormatHelpers

from lib.utils import dt_utcnow
from models import AnalyticsResultsModel, AccountsFilteredModel, AccountsFilteredDetailModel, FollowWatchModel

import csv


class AnalyticsVerticalResultService:

    @classmethod
    def get_list(cls, params):

        _page = get(params, 'page')
        _page_size = get(params, 'page_size')
        _analytic_log_id = get(params, 'analytic_log_id')

        _vertical_result = AnalyticsResultsModel.page(
            filter={
                'analytic_log_id': _analytic_log_id,
                'followers_quality_score': {
                    '$gt': 0
                }
            },
            page=_page,
            page_size=_page_size,
            sort=-1,
            func_sort=lambda x: get(x, 'total_score')
        )

        return _vertical_result

    @classmethod
    def export(cls, params):
        _analytic_log_id = get(params, 'analytic_log_id')

        if not bson.objectid.ObjectId.is_valid(_analytic_log_id):
            raise NotValidObjectIdEx

        _vertical_result = AnalyticsResultsModel.find({
            'analytic_log_id': bson.objectid.ObjectId(_analytic_log_id)
        })

        _vertical_result.sort(key=lambda x: get(x, 'total_score'), reverse=True)

        _filename = f'{dt_utcnow().timestamp()}-{str(_analytic_log_id)}.csv'
        _csv_fieldnames = [
            'Tweeter Id',
            'Username',
            'Name',
            'Verified',
            'Description',
            'Created At',
            'Followers Count',
            'Following Count',
            'Tweet Count',
            'Listed Count',
            'Keyword In Description',
            'Verify Bonus',
            'Engagement Score',
            'Keyword Relevance Score',
            'Followers Quality Score',
            'Recency Score',
            'Total Score'
        ]

        _csv_data = []
        for _item in _vertical_result:
            _data = [
                get(_item, 'id'),
                get(_item, 'username'),
                get(_item, 'name'),
                get(_item, 'verified'),
                get(_item, 'description'),
                datetime.fromtimestamp(get(_item, 'created_at')).strftime('%Y-%m-%d %H:%M:%S'),
                get(_item, 'public_metrics.followers_count'),
                get(_item, 'public_metrics.following_count'),
                get(_item, 'public_metrics.tweet_count'),
                get(_item, 'public_metrics.listed_count'),
                get(_item, 'keyword_in_description'),
                get(_item, 'verify_bonus'),
                get(_item, 'engagement_score'),
                get(_item, 'keyword_relevance_score'),
                get(_item, 'followers_quality_score'),
                get(_item, 'recency_score'),
                get(_item, 'total_score'),
            ]

            _csv_data.append(_data)

        _file_dir = f'public/{_filename}'

        with open(_file_dir, mode='w') as csv_file:
            _writer = csv.writer(csv_file)

            _writer.writerow(_csv_fieldnames)
            _writer.writerows(_csv_data)

        return _file_dir

    @classmethod
    def insert_accounts_filtered(cls, analytic_id, usernames):
        _new_usernames = set(usernames)

        for username in _new_usernames:
            _inserted = AccountsFilteredDetailModel.find_one(
                filter={
                    'username': username
                }
            )
            if _inserted:
                continue

            AccountsFilteredDetailModel.insert_one({
                'id': '',
                'username': username,
                'name': '',
                'verified': False,
                'verified_type': 'none',
                'created_at': 0,
                'public_metrics': {
                    'followers_count': 0,
                    'following_count': 0,
                    'tweet_count': 0,
                    'listed_count': 0,
                },
                'description': '',
                'friendship': [],
                'created_time': dt_utcnow(),
                'created_by': 'services:AnalyticsVerticalResultService:insert_accounts_filtered',
                'updated_time': dt_utcnow(),
                'updated_by': '',
            })

        _inserted = AccountsFilteredModel.find_one(filter={'analytic_id': ObjectId(analytic_id)})
        if not _inserted:
            _result = AccountsFilteredModel.insert_one({
                'analytic_id': ObjectId(analytic_id),
                'accounts': usernames,
                'created_time': dt_utcnow(),
                'created_by': 'services:AnalyticsVerticalResultService:insert_accounts_filtered',
                'updated_time': dt_utcnow(),
                'updated_by': '',
            })

            return get(_result, 'inserted_id')

        _old_usernames = get(_inserted, 'accounts', [])
        _result = list(_new_usernames)
        if _old_usernames:
            _new_username_without_duplicate = set(_old_usernames) - _new_usernames
            _result = _old_usernames + list(_new_username_without_duplicate)
        AccountsFilteredModel.update_one(
            filter={'analytic_id': ObjectId(analytic_id)},
            obj={
                'accounts': _result,
                'updated_time': dt_utcnow(),
                'updated_by': 'services:AnalyticsVerticalResultService:insert_accounts_filtered'
            }
        )
        return get(_inserted, '_id')

    @classmethod
    def insert_account_friendship(cls, account, followers_you_follow):
        _new_followers = set(followers_you_follow)
        _inserted = AccountsFilteredDetailModel.find_one(filter={'username': account})

        if not _inserted:
            _result = AccountsFilteredDetailModel.insert_one({
                'id': '',
                'username': account,
                'name': '',
                'verified': False,
                'verified_type': 'none',
                'created_at': 0,
                'public_metrics': {},
                'description': '',
                'friendship': _new_followers,
                'created_time': dt_utcnow(),
                'created_by': 'services:AnalyticsVerticalResultService:insert_account_friendship',
                'updated_time': dt_utcnow(),
                'updated_by': '',
            })

            return get(_result, 'inserted_id')

        _old_followers = get(_inserted, 'friendship', [])
        _result = list(_new_followers)
        if _old_followers:
            _new_followers_without_duplicate = set(_old_followers) - _new_followers
            _result = _old_followers + list(_new_followers_without_duplicate)
        AccountsFilteredDetailModel.update_one(
            filter={'_id': get(_inserted, '_id')},
            obj={
                'friendship': _result,
                'updated_time': dt_utcnow(),
                'updated_by': 'services:AnalyticsVerticalResultService:insert_account_friendship'
            }
        )
        return get(_inserted, '_id')

    @classmethod
    def update_account_filtered_detail(
            cls,
            username: str,
            name: str,
            description: str,
            verified: bool,
            verified_type: str,
            join: str,
            followers: str,
            following: str,
            tweet_count: str,
            user_url: str,
            user_location: str,
            user_professional_category: str,
    ):
        _inserted = AccountsFilteredDetailModel.find_one(filter={'username': username})
        if not _inserted:
            raise AccountFilteredDetailNotExistedEx

        # parse followers, following
        _followers_count = 0
        if followers:
            _followers_count = FormatHelpers.str_to_num(str_num=followers)
        _following_count = 0
        if following:
            _following_count = FormatHelpers.str_to_num(str_num=following)
        _tweet_count = 0
        if tweet_count:
            _tweet_count = FormatHelpers.str_to_num(str_num=tweet_count)

        if _following_count > 0 or _followers_count > 0:
            FollowWatchModel.insert_one({
                'username': username,
                'followers_count': _followers_count,
                'following_count': _following_count,
                'created_time': dt_utcnow(),
                'created_by': 'services:AnalyticsVerticalResultService:update_account_filtered_detail',
                'updated_time': dt_utcnow(),
                'updated_by': 'services:AnalyticsVerticalResultService:update_account_filtered_detail',
            })

        # parse join time
        _result = FormatHelpers.str_to_date(str_date=join)
        _created_at = get(_result, 'time', 0)

        # verified
        _verified = False
        if verified is not None:
            _verified = verified
        _verified_type = ''
        if verified_type is not None:
            _verified_type = verified_type

        # name, description
        _name = ''
        if name is not None:
            _name = name
        _description = ''
        if description is not None:
            _description = description

        _user_url = ''
        if user_url is not None:
            _user_url = user_url

        _user_location = ''
        if user_location is not None:
            _user_location = user_location

        _user_professional_category = ''
        if user_professional_category is not None:
            _user_professional_category = user_professional_category

        AccountsFilteredDetailModel.update_one(
            filter={'_id': get(_inserted, '_id')},
            obj={
                'name': _name,
                'description': _description,
                'verified': _verified,
                'verified_type': _verified_type,
                'user_url': _user_url,
                'user_location': _user_location,
                'user_professional_category': _user_professional_category,
                'public_metrics': {
                    'followers_count': _followers_count,
                    'following_count': _following_count,
                    'tweet_count': _tweet_count,
                    'listed_count': 0,
                },
                'created_at': _created_at,
                'updated_time': dt_utcnow(),
                'updated_by': 'services:AnalyticsVerticalResultService:update_account_filtered_detail'
            }
        )

        return get(_inserted, '_id')
