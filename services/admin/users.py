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
from exceptions.users import CanOnlyAddUserWithLessRolesEx, UsernameExistedEx
from lib import BadRequest
from lib.enums.roles import Roles, ROLES_WEIGHT
from lib.logger import debug
from lib.security import auth_token_key
from lib.utils import random_str, dt_utcnow
from models import SessionsModel, UsersModel


class AdminUsersService:
    @classmethod
    def _hash_password(cls, password):
        return bcrypt.hashpw(
            password=password.encode("utf-8"), salt=bcrypt.gensalt()
        ).decode("utf-8")

    @classmethod
    def _validate_input_users_roles(cls, login_info, user_role):
        _login_roles = get(login_info, "user.roles", [])
        for _role in _login_roles:
            if get(ROLES_WEIGHT, _role) > get(ROLES_WEIGHT, user_role):
                return True

        raise CanOnlyAddUserWithLessRolesEx

    @classmethod
    def get_list(cls, params):
        _page = get(params, "page")
        _page_size = get(params, "page_size")

        _result = UsersModel.page(
            filter={
                "deleted": False,
            },
            page=_page,
            page_size=_page_size,
            sort=-1,
            func_sort=lambda x: get(x, "created_time", dt_utcnow()),
        )

        return _result

    @classmethod
    def create_users(cls, login_info, form_data):
        _username = get(form_data, "username")
        _password = get(form_data, "password")
        _role = get(form_data, "role")

        cls._validate_input_users_roles(login_info=login_info, user_role=_role)

        _check_user_existed = UsersModel.find_one({"username": _username})

        if _check_user_existed:
            raise UsernameExistedEx

        _hash_password = AdminUsersService._hash_password(password=_password)

        UsersModel.insert_one(
            {
                **form_data,
                "password": _hash_password,
                "roles": [_role],
                "created_by": get(login_info, "user.username"),
            }
        )

        return {}

    @classmethod
    def update_password(cls, user_id, login_info, form_data):
        if not bson.objectid.ObjectId.is_valid(user_id):
            raise NotValidObjectIdEx

        _update_data = {**form_data, "updated_by": get(login_info, "user.username")}
        _password = get(form_data, "password")
        if _password:
            _hash_password = AdminUsersService._hash_password(password=_password)
            _update_data = {
                **_update_data,
                "password": _hash_password,
            }

        UsersModel.update_one({"_id": bson.objectid.ObjectId(user_id)}, _update_data)

        return {}

    # add fields delete user
    @classmethod
    def delete_user_fromDB(cls, user_id, login_info):
        if not bson.objectid.ObjectId.is_valid(user_id):
            raise NotValidObjectIdEx

        print(bson.objectid.ObjectId(user_id))
        print(UsersModel.find_one({"id": bson.objectid.ObjectId(user_id)}))

        UsersModel.update_one(
            {
                "_id": bson.objectid.ObjectId(user_id),
            },
            {
                "deleted": True,
                "deleted_by": get(login_info, "user.username"),
                "updated_by": get(login_info, "user.username"),
            },
        )
        return {"done": True}

    @classmethod
    def delete_user(cls, user_id, login_info):
        _user = UsersModel.find_one({"_id": bson.objectid.ObjectId(user_id)})

        if not _user:
            return {"message": "User not found"}, 404

        user_to_delete_access_token = str(_user["_id"])
        _key = auth_token_key(user=user_to_delete_access_token)

        print("access_token", redis_cluster.get(_key))
        # delete access_token in redis
        check = redis_cluster.delete(_key)
        # delete user in db
        _result = AdminUsersService.delete_user_fromDB(
            user_id=user_id, login_info=login_info
        )

        return _result
