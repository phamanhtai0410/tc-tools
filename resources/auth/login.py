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


class AuthLoginResource(Resource):

    @security.http(
        login_required=False,
        form_data=AuthRequestSchema(),
        response=AuthResponseSchema()
    )
    def post(self, form_data):
        _headers = request.headers
        _result = AuthService.login(form_data=form_data, headers=_headers)
        return _result
