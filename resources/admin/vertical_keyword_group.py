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
from schemas.vertical_keyword_group import ListVerticalKeywordGroupResponseSchema, InputVerticalKeywordGroupRequestSchema
from schemas.request import RequestSchema
from services.admin.users import AdminUsersService
from services.admin.vertical_keyword_group import AdminVerticalKeywordGroupService
from services.auth.auth import AuthService


class AdminVerticalKeywordGroupResource(Resource):

    @security.http(
        login_required=True,
        params=RequestSchema(),
        response=ListVerticalKeywordGroupResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, login_info, params):
        _ids = py_.get(request, 'args.ids', [])
        _result = AdminVerticalKeywordGroupService.get_list(params={
            **params,
            'ids': _ids
        })
        
        return _result

    @security.http(
        login_required=True,
        form_data=InputVerticalKeywordGroupRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info, form_data):
        _result = AdminVerticalKeywordGroupService.create(login_info=login_info, form_data=form_data)
        
        return _result

