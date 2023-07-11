# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from lib.utils import dt_utcnow
from models import FavouriteAccountModel


class AdminFavouriteAcccountService:
        
        
    @classmethod
    def create(cls, login_info, form_data):

        _username = get(form_data, 'username')

        if FavouriteAccountModel.find_one({
            'username': _username,
            'deleted': False
        }):
            raise FavouriteAccountModel

        FavouriteAccountModel.insert_one({
            **form_data,
            'created_by': get(login_info, 'user.username') or 'ADMIN'
        })

        return {}
    
    @staticmethod
    def create_batch_of_accounts(login_info, form_data):
        _usernames = get(form_data, 'usernames')
        for _name in _usernames:
            FavouriteAccountModel.insert_one({
                'username': _name,
                'deleted': False,
                'created_by': get(login_info, 'user.username')
            })
        return {}

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
