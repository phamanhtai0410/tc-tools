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
from slugify import slugify

from config import Config
from connect import web3_providers, redis_cluster
from exceptions.auth import UsernameOrPasswordNotCorrectEx
from exceptions.relevant_group import RelevantGroupNameExistedEx
from exceptions.request import NotValidObjectIdEx
from exceptions.users import UsernameExistedEx
from lib import BadRequest
from lib.enums.roles import Roles
from lib.logger import debug
from lib.security import auth_token_key
from lib.utils import random_str, dt_utcnow
from models import RelevantGroupModel



class AdminRelevantGroupService:

    @classmethod
    def get_list(cls, params):
        _search = get(params, 'search')
        _filter = {
            'deleted': False
        }

        if _search:

            # Search with name regex
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

            # trick to check _search is number -> if true will convert to float and search
            if _search.replace('.', '', 1).isdigit():
                _filter['$or'].append({
                    'weight': float(_search)
                })

        _result = RelevantGroupModel.page(
            filter=_filter,
            page=get(params, 'page'),
            page_size=get(params, 'page_size')
        )

        return _result

    @classmethod
    def create(cls, login_info, form_data):
        _check_exist = RelevantGroupModel.find_one({
            'name': get(form_data, 'name'),
            'deleted': False
        })

        if _check_exist:
            raise RelevantGroupNameExistedEx

        RelevantGroupModel.insert_one({
            **form_data,
            'name_slugify': slugify(get(form_data, 'name')),
            'created_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def update_by_id(cls, relevant_group_id, login_info, form_data):
        if not bson.objectid.ObjectId.is_valid(relevant_group_id):
            raise NotValidObjectIdEx

        RelevantGroupModel.update_one({
            '_id': bson.objectid.ObjectId(relevant_group_id)
        }, {
            **form_data,
            'name_slugify': slugify(get(form_data, 'name')),
            'updated_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def delete_by_id(cls, relevant_group_id, login_info):
        if not bson.objectid.ObjectId.is_valid(relevant_group_id):
            raise NotValidObjectIdEx

        RelevantGroupModel.update_one({
            '_id': bson.objectid.ObjectId(relevant_group_id)
        }, {
            'deleted': True,
            'updated_by': get(login_info, 'user.username')
        })

        return {}