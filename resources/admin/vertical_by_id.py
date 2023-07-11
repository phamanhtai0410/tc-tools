# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.vertical import InputVerticalRequestSchema
from services.admin.vertical import AdminVerticalService


class AdminVerticalByIddResource(Resource):

    @security.http(
        login_required=True,
        form_data=InputVerticalRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, vertical_id, login_info, form_data):
        _result = AdminVerticalService.update_by_id(vertical_id=vertical_id, login_info=login_info, form_data=form_data)
        return _result

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def delete(self, vertical_id, login_info):
        _result = AdminVerticalService.delete_by_id(vertical_id=vertical_id, login_info=login_info)
        return _result

