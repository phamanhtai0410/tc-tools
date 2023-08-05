# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from lib.utils import dt_utcnow
from models import FavouriteAccountModel,ExcludeAccountModel
from exceptions.favourite_account import FavouriteAccountNameExistedEx, FavouriteAccountNameNotExistedEx,FavouriteAccountNoteNotExistedEx
from services.analytics.vertical_result import AnalyticsVerticalResultService

class AdminFavouriteAcccountService:
        
        
    @classmethod
    def create(cls, login_info, username):
        _username = username
        _account =  FavouriteAccountModel.find_one({'username': _username, 'deleted': False})
        print("account : ", _account)
        if _account:
            raise FavouriteAccountNameExistedEx
        try:
            FavouriteAccountModel.update_one(
                filter={
                    'username': _username
                },
                obj={
                    'updated_by': get(login_info, 'user.username') or 'ADMIN',
                    'created_by': get(login_info, 'user.username') or 'ADMIN',
                    'deleted': False
                },
                upsert=True 
            )
            usernames = []
            usernames.append(_username)
            AnalyticsVerticalResultService.insert_accounts_filtered(
                analytic_id='647d4683c03a0c62921177c2',
                usernames=usernames
            )
            
        except Exception as e:
            return {'error': str(e)}
        return {}
    
    @staticmethod
    def create_batch_of_accounts(login_info, username):
        _usernames = username

    #     for _name in _usernames:
    #         FavouriteAccountModel.insert_one({
    #             'username': _name,
    #             'deleted': False,
    #             'created_by': get(login_info, 'user.username')
    #         })
    #     return {}


    # @classmethod
    # def delete(cls, login_info, username):
    #     _username = username
    #     # print(_username)
    #     account = FavouriteAccountModel.find_one({'username': _username, 'deleted': False})
    #     if not account:
    #         raise FavouriteAccountNameNotExistedEx

    #     # print(account)
    #     try:
    #         FavouriteAccountModel.update_one(
    #             {
    #                 'username': _username
    #             },
    #             {
    #                 'deleted': True,
    #                 'updated_by': get(login_info, 'user.username') or 'ADMIN'
    #             }
    #         )
            
    #         return {}
    #     except Exception as e:
    #         return {'error': str(e)}
        
    @classmethod
    def delete(cls, login_info,username):
        _username = username
        account = FavouriteAccountModel.find_one({'username': _username, 'deleted': False})
        if not account:
            raise FavouriteAccountNameNotExistedEx
        try:
            FavouriteAccountModel.update_one(
                {
                    'username': _username
                        
                },
                {
                    'deleted': True,
                    'updated_by': get(login_info, 'user.username') or 'ADMIN',
                }
            )
            ExcludeAccountModel.update_one(
                {
                    'username':_username
                },
                {
                    'deleted':False,
                    'updated_by': get(login_info, 'user.username') or 'ADMIN',
                    'create_by':get(login_info, 'user.username') or 'ADMIN',
                },
                upsert=True
            )
            return {}
        except Exception as e:
            return {'error': str(e)}

    @classmethod
    def put(cls, login_info, form_data,username):
        _note = get(form_data,'note')
        _username = username
        account = FavouriteAccountModel.find_one({'username': _username})
        if not account:
            raise FavouriteAccountNameNotExistedEx
        try:
            FavouriteAccountModel.update_one(
                {
                    'username': _username
                        
                },
                {
                    'note':_note,
                    'updated_by': get(login_info, 'user.username') or 'ADMIN',
                }
            )              
            return {}
        except Exception as e:
            return {'error': str(e)}

    @classmethod
    def get(cls,username):
        _username = username
        account = FavouriteAccountModel.find_one({'username': _username})
        if not account:
            raise FavouriteAccountNameNotExistedEx
        else:
            if not account['note']:
                raise FavouriteAccountNoteNotExistedEx
            else:
                return account

            

        
            

        

        


    # @classmethod
    # def update_by_id(cls, follower_group_id, login_info, form_data):
    #     if not bson.objectid.ObjectId.is_valid(follower_group_id):
    #         raise NotValidObjectIdEx

    #     _name = get(form_data, 'name')

    #     if FollowerGroupModel.find_one({
    #         'name': _name,
    #         '_id': {
    #             '$ne': bson.objectid.ObjectId(follower_group_id)
    #         },
    #         'deleted': False
    #     }):
    #         raise FollowerGroupNotExistedEx

    #     FollowerGroupModel.update_one({
    #         '_id': bson.objectid.ObjectId(follower_group_id)
    #     }, {
    #         **form_data,
    #         'name_slugify': slugify(get(form_data, 'name')),
    #         'updated_by': get(login_info, 'user.username')
    #     })

    #     return {}

    # @classmethod
    # def delete(cls, follower_group_id, login_info):
    #     if not bson.objectid.ObjectId.is_valid(follower_group_id):
    #         raise NotValidObjectIdEx

    #     FollowerGroupModel.update_one({
    #         '_id': bson.objectid.ObjectId(follower_group_id)
    #     }, {
    #         'deleted': True,
    #         'updated_by': get(login_info, 'user.username')
    #     })

    #     return {}
