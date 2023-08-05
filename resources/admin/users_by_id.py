# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request
from connect import redis_cluster

from connect import security
from lib.enums.roles import Roles
from schemas.users import (
    UpdateUserPasswordRequestSchema,
    UserSchema,
    CreateUserRequestSchema,
    ListUserResponseSchema,
)
from schemas.request import RequestSchema
from services.admin.users import AdminUsersService
from services.auth.auth import AuthService


class AdminUsersByIdResource(Resource):
    @security.http(
        login_required=True,
        form_data=UpdateUserPasswordRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN],
    )
    def put(self, user_id, login_info, form_data):
        _result = AdminUsersService.update_password(
            user_id=user_id, login_info=login_info, form_data=form_data
        )
        return _result

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN],
    )
    def delete(self, user_id, login_info):
        print("user_id", user_id)
        _result = AdminUsersService.delete_user(user_id=user_id, login_info=login_info)
        return {"message": "Delete user successfully!"}
