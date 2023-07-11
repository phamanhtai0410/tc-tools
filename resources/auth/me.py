# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from schemas.auth.auth import AuthRequestSchema, AuthResponseSchema
from services.auth.auth import AuthService


class AuthMeResource(Resource):

    @security.http(
        login_required=True,
    )
    def get(self, login_info):
        _result = AuthService.get_me(login_info=login_info)
        return _result
