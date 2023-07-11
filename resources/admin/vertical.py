# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.vertical import InputVerticalRequestSchema, ListVerticalResponseSchema
from schemas.request import RequestSchema
from services.admin.relevant_group import AdminRelevantGroupService
from services.admin.vertical import AdminVerticalService


class AdminVerticalResource(Resource):

    @security.http(
        login_required=True,
        params=RequestSchema(),
        response=ListVerticalResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, login_info, params):
        _result = AdminVerticalService.get_list(params=params)
        return _result

    @security.http(
        login_required=True,
        form_data=InputVerticalRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info, form_data):
        AdminVerticalService.create(form_data=form_data, login_info=login_info)
        return {}

