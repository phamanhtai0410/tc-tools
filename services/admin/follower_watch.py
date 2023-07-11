# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from lib.utils import dt_utcnow
from models import FollowWatchModel, FavouriteAccountModel


class AdminFollowerWatchService:
    
    @classmethod
    def get_list(cls, params):
        
        
        _page = get(params, 'page')
        _page_size = get(params, 'page_size')
        _search = get(params, 'search')
        _sort_field = get(params, 'sort_field')
        _sort_direction = get(params, 'sort_direction')

        _filter = {
            'deleted': False
        }
        
        if _search:
            _filter = {
                **_filter,
                'username': {
                    '$regex': _search, '$options': 'i'
                }
            }
            
        _list_favourite_accounts = list(FavouriteAccountModel.find(_filter))
        _usernames = [_item['username'] for _item in _list_favourite_accounts]
        print(_usernames)
        
        _watch_history_list = []
        for _username in _usernames:
            
            _watch_history = list(FollowWatchModel.col.aggregate([
                {
                    '$match': {
                        'deleted': False,
                        'username': _username
                    }    
                },
                {
                    '$group': {
                        '_id': '$username',
                        'followers_count_list': {
                            '$push': '$followers_count'
                        },
                        'total': {
                            '$last': '$followers_count'
                        },
                        'watch_time_list': {
                            '$push': '$created_time'
                        }
                    }    
                }
            ]))
            # print(f"UserName # '{_username}' with data {_watch_history}")
            _watch_history_list.append(_watch_history[0] if len(_watch_history) > 0 else {})
        # print('Watch History List : ', _watch_history_list)        
        _returns = []
        for _item in _watch_history_list:
            _return = {}
            _return['username'] = get(_item, '_id', '')
            _return['total'] = get(_item, 'total', 0)
            _watch_time_list = get(_item, 'watch_time_list', [])
            if len(_watch_time_list) <= 1:
                _return = {
                    **_return,
                    'percent_1d': 0.0,
                    'amount_1d': 0,
                    'percent_3d': 0.0,
                    'percent_7d': 0.0
                }
            else:
                _accumulations = cls.get_accumulation_in_recent_period(
                    get(_item, 'followers_count_list'),
                    get(_item, 'watch_time_list'),
                    get(_item, 'total')
                )
                _return = {
                    **_return,
                    **_accumulations
                }
                    
            _returns.append(_return)
            
        if _sort_field:
            _sort_func = lambda x: get(x, _sort_field)
            if _sort_direction == 'asc':
                _reverse = False
            else:
                _reverse = True
        else:
            _sort_func = None
        if _sort_func:    
            _returns.sort(key=_sort_func, reverse=_reverse)
        _paging_returns = _returns[(_page - 1) * _page_size : _page * _page_size]

        print('** RETURNS = ', _paging_returns)
        
        num_of_page = (len(_returns) /_page_size)
        return {
            'items': _paging_returns,
            'num_of_page': num_of_page,
            'page_size': _page_size,
            'page': _page
        }

    @staticmethod
    def get_accumulation_in_recent_period(followers_count_list=[], watch_time_list=[], current_count=0):
        _now = int(dt_utcnow().timestamp())
        _lastest_watch_1d = _now - 86400 * 365
        _lastest_index_watch_1d = -1
        _lastest_watch_3d = _now - 86400 * 365
        _lastest_index_watch_3d = -1
        _lastest_watch_7d = _now - 86400 * 365
        _lastest_index_watch_7d = -1
        
        for _index, _time in enumerate(watch_time_list):
            if int(_time.timestamp()) > _lastest_watch_1d and int(_time.timestamp()) < _now - 86400 * 1:
                _lastest_watch_1d = int(_time.timestamp())
                _lastest_index_watch_1d = _index
            if int(_time.timestamp()) > _lastest_watch_3d and int(_time.timestamp()) < _now - 86400 * 3:
                _lastest_watch_3d = int(_time.timestamp())
                _lastest_index_watch_3d = _index
            if int(_time.timestamp()) > _lastest_watch_7d and int(_time.timestamp()) < _now - 86400 * 7:
                _lastest_watch_7d = int(_time.timestamp())
                _lastest_index_watch_7d = _index
            
        _return = {}
        if _lastest_index_watch_1d == -1:
            _return['percent_1d'] = 0
            _return['amount_1d'] = 0
        else:
            _return['percent_1d'] = 0 if followers_count_list[_lastest_index_watch_1d] * 100 == 0 else round((current_count - followers_count_list[_lastest_index_watch_1d]) / followers_count_list[_lastest_index_watch_1d] * 100, 2)
            _return['amount_1d'] = current_count - followers_count_list[_lastest_index_watch_1d]
        
        if _lastest_index_watch_3d == -1:
            _return['percent_3d'] = 0
        else:
            _return['percent_3d'] = 0 if followers_count_list[_lastest_index_watch_3d] * 100 == 0 else round((current_count - followers_count_list[_lastest_index_watch_3d]) / followers_count_list[_lastest_index_watch_3d] * 100, 2)
    
        if _lastest_index_watch_7d == -1:
            _return['percent_7d'] = 0
        else:
            _return['percent_7d'] = 0 if followers_count_list[_lastest_index_watch_7d] * 100 == 0 else round((current_count - followers_count_list[_lastest_index_watch_7d]) / followers_count_list[_lastest_index_watch_7d] * 100, 2)
        return _return

        
        
