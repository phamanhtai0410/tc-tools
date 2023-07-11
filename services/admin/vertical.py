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
from exceptions.relevant_group import RelevantGroupNameExistedEx, RelevantGroupNotFoundEx
from exceptions.request import NotValidObjectIdEx
from exceptions.users import UsernameExistedEx
from exceptions.analytics import VerticalNameExistedEx
from lib import BadRequest
from lib.enums.roles import Roles
from lib.logger import debug
from lib.security import auth_token_key
from lib.utils import random_str, dt_utcnow
from models import RelevantGroupModel, VerticalModel



class AdminVerticalService:

    @classmethod
    def _validate_relevant_group(cls, form_data):
        for _key in get(form_data, 'keywords'):
            _relevant_group_id = get(_key, 'relevant_group_id')
            print(_relevant_group_id)
            if not bson.objectid.ObjectId.is_valid(_relevant_group_id) or not RelevantGroupModel.find_one({
                '_id': bson.objectid.ObjectId(_relevant_group_id),
                'deleted': False
            }):
                raise RelevantGroupNotFoundEx

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

        _result = VerticalModel.page(
            filter=_filter,
            page=get(params, 'page'),
            page_size=get(params, 'page_size')
        )

        return _result

    @classmethod
    def create(cls, login_info, form_data):
        _check_exist = VerticalModel.find_one({
            'name': get(form_data, 'name'),
            'deleted': False
        })

        if _check_exist:
            raise VerticalNameExistedEx

        cls._validate_relevant_group(form_data=form_data)

        VerticalModel.insert_one({
            **form_data,
            'name_slugify': slugify(get(form_data, 'name')),
            'created_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def update_by_id(cls, vertical_id, login_info, form_data):
        if not bson.objectid.ObjectId.is_valid(vertical_id):
            raise NotValidObjectIdEx

        cls._validate_relevant_group(form_data=form_data)

        VerticalModel.update_one({
            '_id': bson.objectid.ObjectId(vertical_id)
        }, {
            **form_data,
            'name_slugify': slugify(get(form_data, 'name')),
            'updated_by': get(login_info, 'user.username')
        })

        return {}

    @classmethod
    def delete_by_id(cls, vertical_id, login_info):
        if not bson.objectid.ObjectId.is_valid(vertical_id):
            raise NotValidObjectIdEx

        VerticalModel.update_one({
            '_id': bson.objectid.ObjectId(vertical_id)
        }, {
            'deleted': True,
            'updated_by': get(login_info, 'user.username')
        })

        return {}