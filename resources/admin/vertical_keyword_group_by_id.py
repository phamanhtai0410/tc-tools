# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.vertical_keyword_group import ListVerticalKeywordGroupResponseSchema, InputVerticalKeywordGroupRequestSchema
from schemas.request import RequestSchema
from services.admin.users import AdminUsersService
from services.admin.vertical_keyword_group import AdminVerticalKeywordGroupService
from services.auth.auth import AuthService


class AdminVerticalKeywordGroupByIdResource(Resource):

    @security.http(
        login_required=True,
        form_data=InputVerticalKeywordGroupRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, vertical_keyword_group_id, login_info, form_data):
        _result = AdminVerticalKeywordGroupService.update_by_id(vertical_keyword_group_id=vertical_keyword_group_id, login_info=login_info, form_data=form_data)
        return _result

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def delete(self, vertical_keyword_group_id, login_info):
        _result = AdminVerticalKeywordGroupService.delete(vertical_keyword_group_id=vertical_keyword_group_id, login_info=login_info)
        return _result
