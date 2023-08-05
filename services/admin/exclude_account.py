# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from lib.utils import dt_utcnow
from models import FavouriteAccountModel,ExcludeAccountModel
from exceptions.exclude_account import AccountNameExistedEx,AccountNameNotExistedEx

class ExcludeAcccountService:
    @classmethod
    def post(cls, login_info, username):
        _username = username
        try:
            ExcludeAccountModel.update_one(
                filter={
                    'username': _username
                },
                obj={
                    # 'updated_by': get(login_info, 'user.username') or 'ADMIN',
                    'created_by': get(login_info, 'user.username') or 'ADMIN',
                    'deleted': False
                },
                upsert=True
            )
        except Exception as e:
            return {'error': str(e)}
        return {}

    @classmethod
    def delete(cls, login_info,username):
        _username = username
        account = ExcludeAccountModel.find_one({'username': _username, 'deleted': False})
        if not account:
            raise AccountNameNotExistedEx
        try:
            ExcludeAccountModel.update_one(
                {
                    'username': _username
                        
                },
                {
                    'deleted': True,
                    'updated_by': get(login_info, 'user.username') or 'ADMIN',
                }
            )
            return {}
        except Exception as e:
            return {'error': str(e)}
    
        
        