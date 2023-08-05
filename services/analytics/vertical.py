# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import copy

from bson import ObjectId
from pydash import get, set_
import bson
from slugify import slugify
import pydash as py_

from exceptions.follower_group import FollowerGroupNotExistedEx
from exceptions.request import NotValidObjectIdEx
from exceptions.analytics import AnalyticsNotFoundEx, AnalyticsVerticalKeywordGroupCanNotDuplicateEx, \
    AnalyticsVerticalNameExistedEx, VerticalNameExistedEx, VerticalNotFoundEx
from exceptions.vertical_keyword_group import VerticalKeywordGroupNotExistedEx, KeywordURLNotExistedEx, \
    AccountProfileLinkNotExistedEx
from lib.enums.task_status import TaskStatus
from lib.utils import random_str, dt_utcnow
from models import AnalyticsLogsModel, AnalyticsModel, FollowerGroupModel, RelevantGroupModel, \
    VerticalKeywordGroupModel, VerticalModel, KeywordSearchLinkModel, AccountsFilteredDetailModel, FavouriteAccountModel, ExcludeAccountModel


class AnalyticsVerticalService:

    @classmethod
    def _validate_vertical_keyword_groups(cls, vertical_keyword_groups):
        # validate group keywords
        for (_idx, _vertical_keyword_id) in enumerate(vertical_keyword_groups):
            if not bson.objectid.ObjectId.is_valid(_vertical_keyword_id) or not VerticalKeywordGroupModel.find_one({
                '_id': bson.objectid.ObjectId(_vertical_keyword_id),
                'deleted': False
            }):
                raise VerticalKeywordGroupNotExistedEx

            if py_.find_index(vertical_keyword_groups, lambda x: x == _vertical_keyword_id) != _idx:
                raise AnalyticsVerticalKeywordGroupCanNotDuplicateEx

    @classmethod
    def _validate_follower_group(cls, follower_group_id):
        # validate group keywords
        if not bson.objectid.ObjectId.is_valid(follower_group_id) or not FollowerGroupModel.find_one({
            '_id': bson.objectid.ObjectId(follower_group_id),
            'deleted': False
        }):
            raise FollowerGroupNotExistedEx

    @classmethod
    def _validate_analytics_existed(cls, analytics_vertical_id):
        if not bson.objectid.ObjectId.is_valid(analytics_vertical_id):
            raise NotValidObjectIdEx

        _analytics = AnalyticsModel.find_one({
            '_id': bson.objectid.ObjectId(analytics_vertical_id)
        })

        if not _analytics:
            raise AnalyticsNotFoundEx

        return _analytics

    @classmethod
    def _mapping_analytics_vertical(cls, items):
        return items

    @classmethod
    def _mapping_vertical_keyword_group(cls, vertical_keyword_groups):
        _vertical_keyword_group_data = []
        for _vertical_keyword_id in vertical_keyword_groups:
            _vertical_keyword_group = VerticalKeywordGroupModel.find_one({
                '_id': _vertical_keyword_id
            })
            _vertical_keyword_group_data.append(_vertical_keyword_group)

        return _vertical_keyword_group_data

    @classmethod
    def _mapping_follower_group(cls, follower_group_id):
        _follower_group = FollowerGroupModel.find_one({
            '_id': follower_group_id
        })

        return _follower_group



    @classmethod
    def get_list_default(cls):
        temp = AnalyticsModel.find_one(filter={"vertical_name":"analytics_default"})
        pipeline = [
             
                 {
                     "$match":{
                      "deleted": {"$ne": True} 
                    }
                 },
                 {
                      "$group": {
                          "_id": "$username"
                     }
                 },
               
             
        ]
        result = list(ExcludeAccountModel.col.aggregate(pipeline))
        result_list = [i['_id'] for i in result]
        temp['exclude_account']  =result_list
        return temp
    
    @classmethod
    def edit(cls,login_info,form_data):
        AnalyticsModel.find_one(filter={"vertical_name":"analytics_default"})

        cls._validate_vertical_keyword_groups(vertical_keyword_groups=get(form_data, 'vertical_keyword_groups'))

        cls._validate_follower_group(follower_group_id=get(form_data, 'follower_group_id'))

        _vertical_keywords = cls._mapping_vertical_keyword_group(
            vertical_keyword_groups=get(form_data, 'vertical_keyword_groups'))

        _follower_group = cls._mapping_follower_group(follower_group_id=get(form_data, 'follower_group_id'))

        _exclude_account = get(form_data,'exclude_account')
        for i in _exclude_account:
            if i != None:
                 ExcludeAccountModel.update_one(
                      filter={'username': i},
                      obj={
                             'username': i,
                             'updated_by': get(login_info, 'user.username') or 'ADMIN',
                             'created_by': get(login_info, 'user.username') or 'ADMIN',
                             'deleted': False
                      },
                      upsert=True          
            )
        exclude_filter ={
                            "username": {"$nin": [i for i in _exclude_account]},
                            "deleted": False
                        }
        excluded_accounts = ExcludeAccountModel.find(filter=exclude_filter)
        for i in excluded_accounts:
            ExcludeAccountModel.update_one(
                filter={'username': i['username']},
                obj={
                          'updated_by': get(login_info, 'user.username') or 'ADMIN',
                          'created_by': get(login_info, 'user.username') or 'ADMIN',
                          'deleted': True
                    }
            )
        
        

        AnalyticsModel.update_one({
            'vertical_name': "analytics_default"
        }, {
            **form_data,
            'follower_group': _follower_group,
            'vertical_keywords': _vertical_keywords,
            # 'vertical_name_slugify': slugify(get(form_data, 'vertical_name')),
            'updated_by': get(login_info, 'user.username')
        })
        return
        

    
    @classmethod
    def get_list(cls, params):
        _search = get(params, 'search')
        _filter = {
            'deleted': False
        }

        if _search:
            _filter = {
                **_filter,
                '$or': [
                    {
                        'vertical_name': {
                            '$regex': _search, '$options': 'i'
                        }
                    },
                    {
                        'name_slugify': {
                            '$regex': _search, '$options': 'i'
                        }
                    }
                ]
            }

        _result = AnalyticsModel.page(
            filter=_filter,
            page=get(params, 'page'),
            page_size=get(params, 'page_size'),
            sort=-1,
            func_sort=lambda x: get(x, 'created_time', dt_utcnow())
        )

        return _result

    @classmethod
    def create(cls, login_info, form_data):
        # validate vertical_name
        _vertical_name = get(form_data, 'vertical_name')

        if AnalyticsModel.find_one({
            'vertical_name': _vertical_name,
            'deleted': False
        }):
            raise AnalyticsVerticalNameExistedEx

        cls._validate_vertical_keyword_groups(vertical_keyword_groups=get(form_data, 'vertical_keyword_groups'))

        cls._validate_follower_group(follower_group_id=get(form_data, 'follower_group_id'))

        _vertical_keywords = cls._mapping_vertical_keyword_group(
            vertical_keyword_groups=get(form_data, 'vertical_keyword_groups'))

        _follower_group = cls._mapping_follower_group(follower_group_id=get(form_data, 'follower_group_id'))

        _inserted = AnalyticsModel.insert_one({
            **form_data,
            'follower_group': _follower_group,
            'vertical_keywords': _vertical_keywords,
            'vertical_name_slugify': slugify(get(form_data, 'vertical_name')),
            'created_by': get(login_info, 'user.username')
        })

        return get(_inserted, '_id')

    @classmethod
    def update_by_id(cls, analytics_vertical_id, login_info, form_data):
        # validate vertical_name
        _analytics = cls._validate_analytics_existed(analytics_vertical_id=analytics_vertical_id)

        _vertical_name = get(form_data, 'vertical_name')

        if AnalyticsModel.find_one({
            'vertical_name': _vertical_name,
            '_id': {
                '$ne': bson.objectid.ObjectId(analytics_vertical_id)
            },
            'deleted': False
        }):
            raise AnalyticsVerticalNameExistedEx

        cls._validate_vertical_keyword_groups(vertical_keyword_groups=get(form_data, 'vertical_keyword_groups'))

        cls._validate_follower_group(follower_group_id=get(form_data, 'follower_group_id'))

        _vertical_keywords = cls._mapping_vertical_keyword_group(
            vertical_keyword_groups=get(form_data, 'vertical_keyword_groups'))

        _follower_group = cls._mapping_follower_group(follower_group_id=get(form_data, 'follower_group_id'))

        AnalyticsModel.update_one({
            '_id': bson.objectid.ObjectId(analytics_vertical_id)
        }, {
            **form_data,
            'follower_group': _follower_group,
            'vertical_keywords': _vertical_keywords,
            'vertical_name_slugify': slugify(get(form_data, 'vertical_name')),
            'updated_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def delete(cls, analytics_vertical_id, login_info):
        _analytics = cls._validate_analytics_existed(analytics_vertical_id=analytics_vertical_id)
        AnalyticsModel.update_one({
            '_id': bson.objectid.ObjectId(analytics_vertical_id)
        }, {
            'deleted': True,
            'updated_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def get_list_log(cls, params):
        _search = get(params, 'search')
        _filter = {
            'deleted': False
        }

        if _search:
            _filter = {
                **_filter,
                '$or': [
                    {
                        'vertical_name': {
                            '$regex': _search, '$options': 'i'
                        }
                    },
                    {
                        'name_slugify': {
                            '$regex': _search, '$options': 'i'
                        }
                    }
                ]
            }

        _result = AnalyticsLogsModel.page(
            filter=_filter,
            page=get(params, 'page'),
            page_size=get(params, 'page_size'),
            sort=-1,
            func_sort=lambda x: get(x, 'created_time', dt_utcnow())
        )

        return _result

    @classmethod
    def run(cls, analytics_vertical_id, login_info):
        _analytics = cls._validate_analytics_existed(analytics_vertical_id=analytics_vertical_id)

        _analytics_id = copy.deepcopy(get(_analytics, '_id'))

        del _analytics['_id']

        AnalyticsLogsModel.update_one({
            'analytics_id': _analytics_id,
        },
            {
                **_analytics,
                'analytics_id': _analytics_id,
                'status': TaskStatus.PENDING,
                'updated_by': get(login_info, 'user.username')
            }, upsert=True)

        return {}
    
    @classmethod
    def update_favorite(cls):
        favoriteAcc =FavouriteAccountModel.find(
            filter={"deleted":False}
        )
     
        result = {'username': []}
        
        for json_obj in favoriteAcc:
            username = json_obj.get('username')
            if username is not None:
                result['username'].append(username)
                
        for i in result['username']:
            AccountsFilteredDetailModel.update_one(
                filter={'username': i},
                obj={
                    'check_crawl': False,
                    'updated_by': 'services:AnalyticsVerticalResultService:update_account_filtered_detail'
                }
            )      
     
    @classmethod
    def get_keyword_url(cls):

        _cursors = KeywordSearchLinkModel.col.aggregate([
            {
                '$match': {
                    'is_used': False
                }
            },
            {
                '$sample': {
                    'size': 1
                }
            }
        ])

        _keyword_url = get(list(_cursors), '[0]')

        if not _keyword_url:
            raise KeywordURLNotExistedEx

        KeywordSearchLinkModel.update_one(
            filter={
                '_id': get(_keyword_url, '_id')
            },
            obj={
                'is_used': True,
                'updated_time': dt_utcnow(),
                'updated_by': 'services:AnalyticsVerticalService:get_keyword_url'
            }
        )

        return {
            'analytic_id': str(get(_keyword_url, 'analytic_id')),
            'keyword': get(_keyword_url, 'keyword'),
            'url': get(_keyword_url, 'url')
        }
    
    @classmethod
    def remove_key(cls,form_data):
        obj = form_data['key_remove']
        _keyword_url = KeywordSearchLinkModel.find_one(
            filter={
                'keyword':obj

            }

        )
        if not _keyword_url:
            raise KeywordURLNotExistedEx
        
        KeywordSearchLinkModel.update_one(
            filter={
                'keyword': get(_keyword_url, 'keyword')
            },
            obj={
                'deleted': True,
                 'updated_by': 'services:AnalyticsVerticalService:get_keyword_url'

 
            }
        )

        return

    @classmethod
    def is_used_false(cls):
        KeywordSearchLinkModel.update_many(
            filter={'deleted':False},
            obj={
                'is_used':False,
                "updated_by": "Crontab"
            }            
        )
        return

        
    @classmethod
    def add_key(cls,form_data, login_info):
        obj = form_data['key_add']
        _keyword_url = KeywordSearchLinkModel.find_one(
            filter={
                'keyword':obj

            }

        )
        if not _keyword_url:
            url = 'https://twitter.com/search?q='+obj+'&src=typed_query'
            print(obj)
            print(url)
            _id = KeywordSearchLinkModel.insert_one({
                'keyword': obj,
                'is_used':False,
                'deleted': False,
                'created_by': get(login_info, 'user.username') or "admin",
                'url': url,
            })
            print("ss", _id)
            return
        
        KeywordSearchLinkModel.update_one(
            filter={
                'keyword': get(_keyword_url, 'keyword')
            },
            obj={
                'deleted': False,
                 'updated_by': 'services:AnalyticsVerticalService:get_keyword_url'
            }
        )

        return

 

    @classmethod
    def get_account_profile_link(cls):
        _cursors = AccountsFilteredDetailModel.col.aggregate([
            {
                '$match': {
                    'check_crawl':False  
                }
            },
            {
                '$sample': {
                    'size': 1
                }
            }
        ])

        _account_detail = get(list(_cursors), '[0]')

        if not _account_detail:
            raise AccountProfileLinkNotExistedEx

        return {
            'account': get(_account_detail, 'username'),
            'url': f"https://twitter.com/{get(_account_detail, 'username')}"
        }

    @classmethod
    def get_follower_you_follow_link(cls):
        _cursors = AccountsFilteredDetailModel.col.aggregate([
            {
                '$match': {
                    'check_friendship': False,
                    "created_at": {"$gte": 1672531200 },
                    "description": {"$ne": ""}
                }
            },
            {
                '$sample': {
                    'size': 1
                }
            }
        ])

        _account_detail = get(list(_cursors), '[0]')

        if not _account_detail:
            raise AccountProfileLinkNotExistedEx

        AccountsFilteredDetailModel.update_one(
            filter={'_id': get(_account_detail, '_id')},
            obj={
                'check_friendship': True,
                'updated_time': dt_utcnow(),
                'updated_by': 'services:AnalyticsVerticalService:get_follower_you_follow_link'
            }
        )

        return {
            'account': get(_account_detail, 'username'),
            'url': f"https://twitter.com/{get(_account_detail, 'username')}/followers_you_follow"
        }
        
    @classmethod
    def checkurl(cls):
        _keyword_url = KeywordSearchLinkModel.find_one(
            filter={
                'is_used': False
            }
        )
        
        if  _keyword_url:
            url = _keyword_url['url']
            KeywordSearchLinkModel.update_one(
            filter={
                'url': url
            },
            obj={
                'is_used': True,
                'updated_time': dt_utcnow(),
                'updated_by': 'services:AnalyticsVerticalService:get_keyword_url'
            }
        )
            return url
        return 1


    @classmethod
    def checkfolow(cls):
       folow_profile = AccountsFilteredDetailModel.find_one(
            filter={
                 'check_friendship': False,
                 "created_at": {"$gte": 1672531200 },
                 "description": {"$ne": ""}
            }
       )
       if  folow_profile:
            url='https://twitter.com/'
            url = url + folow_profile['username']+'/followers_you_follow'
            return url
       return 3


    @classmethod
    def checkprofile(cls):
        _profile = AccountsFilteredDetailModel.find_one(
              filter={
                'check_crawl': False
            }
        )
        print(_profile)
        if _profile:
            url = 'https://twitter.com/'
            url = url+_profile['username']
            return url
        return 2