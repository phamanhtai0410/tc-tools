# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request
import pydash as py_

from connect import security
from lib.enums.roles import Roles
from schemas.exclude_account import InputExcludeAccountsRequestSchema
from services.admin.exclude_account import ExcludeAcccountService

class AdminExcludeAccountResource(Resource):
    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, username, login_info):
        _result = ExcludeAcccountService.post(login_info=login_info, username=username)
        return _result
    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def delete(self, username, login_info):
        _result = ExcludeAcccountService.delete(login_info=login_info, username=username)
        return _result