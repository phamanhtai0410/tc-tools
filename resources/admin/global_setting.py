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
from schemas.global_setting import GlobalSettingSchema, InputGlobalSettingRequestSchema, ListGlobalSettingResponseSchema
from schemas.request import RequestSchema
from services.admin.global_setting import AdminGlobalSettingService


class AdminGlobalSettingResource(Resource):

    @security.http(
        login_required=True,
        response=GlobalSettingSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, login_info):
        _result = AdminGlobalSettingService.get()

        return _result

    @security.http(
        login_required=True,
        form_data=InputGlobalSettingRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, login_info, form_data):
        _result = AdminGlobalSettingService.update(login_info=login_info, form_data=form_data)

        return _result
