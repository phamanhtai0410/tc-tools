# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import string
from datetime import timedelta

import jwt
import bcrypt
from pydash import get
import bson

from config import Config
from connect import web3_providers, redis_cluster
from exceptions.auth import UsernameOrPasswordNotCorrectEx
from exceptions.request import NotValidObjectIdEx
from exceptions.users import UsernameExistedEx
from exceptions.vertical_keyword_group import VerticalKeywordGroupNameExistedEx
from lib import BadRequest
from lib.enums.roles import Roles
from lib.logger import debug
from lib.security import auth_token_key
from lib.utils import random_str, dt_utcnow
from models import SessionsModel, UsersModel, VerticalKeywordGroupModel
from slugify import slugify

class AdminVerticalKeywordGroupService:

    @classmethod
    def get_list(cls, params):
        _page = get(params, 'page')
        _page_size = get(params, 'page_size')
        _search  = get(params, 'search')
        _ids =  get(params, 'ids')
        
        _filter = {
            'deleted': False
        }

        if _ids:
            _filter = {
                **_filter,
                '_id': {
                    '$in': [bson.objectid.ObjectId(x) for x in _ids.split(',')]
                }
            }

        elif _search:
            _filter = {
                **_filter,
                '$or': [
                    {
                        'name': {
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

        if _ids:
            _items = VerticalKeywordGroupModel.find(_filter)
            _result = {
                'items': _items
            }
        else:
            _result = VerticalKeywordGroupModel.page(
                filter=_filter,
                page=_page,
                page_size=_page_size,
                sort=-1,
                func_sort=lambda x: get(x, 'created_time', dt_utcnow())
            )

        return _result

    @classmethod
    def create(cls, login_info, form_data):

        _name = get(form_data, 'name')

        if VerticalKeywordGroupModel.find_one({
            'name': _name,
            'deleted': False
        }):
            raise VerticalKeywordGroupNameExistedEx

        VerticalKeywordGroupModel.insert_one({
            **form_data,
            'name_slugify': slugify(get(form_data, 'name')),
            'created_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def update_by_id(cls, vertical_keyword_group_id, login_info, form_data):
        if not bson.objectid.ObjectId.is_valid(vertical_keyword_group_id):
            raise NotValidObjectIdEx

        _name = get(form_data, 'name')

        if VerticalKeywordGroupModel.find_one({
            'name': _name,
            '_id': {
                '$ne': bson.objectid.ObjectId(vertical_keyword_group_id)
            },
            'deleted': False
        }):
            raise VerticalKeywordGroupNameExistedEx

        VerticalKeywordGroupModel.update_one({
            '_id': bson.objectid.ObjectId(vertical_keyword_group_id)
        }, {
            **form_data,
            'name_slugify': slugify(get(form_data, 'name')),
            'updated_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def delete(cls, vertical_keyword_group_id, login_info):
        if not bson.objectid.ObjectId.is_valid(vertical_keyword_group_id):
            raise NotValidObjectIdEx

        VerticalKeywordGroupModel.update_one({
            '_id': bson.objectid.ObjectId(vertical_keyword_group_id)
        }, {
            'deleted': True,
            'updated_by': get(login_info, 'user.username')
        })

        return {}
