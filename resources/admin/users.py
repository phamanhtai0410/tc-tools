# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.users import UserSchema, CreateUserRequestSchema, ListUserResponseSchema
from schemas.request import RequestSchema
from services.admin.users import AdminUsersService
from services.auth.auth import AuthService


class AdminUsersResource(Resource):
    @security.http(
        login_required=True,
        params=RequestSchema(),
        response=ListUserResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN],
    )
    def get(self, login_info, params):
        _result = AdminUsersService.get_list(params=params)
        return _result

    @security.http(
        login_required=True,
        form_data=CreateUserRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN],
    )
    def post(self, login_info, form_data):
        _result = AdminUsersService.create_users(
            login_info=login_info, form_data=form_data
        )
        return _result
