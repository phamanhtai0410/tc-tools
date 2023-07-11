# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.analytics.vertical import ListAnalyticsVerticalResponseSchema, AnalyticsVerticalRequestSchema
from schemas.request import RequestSchema
from services.admin.vertical import AdminVerticalService
from services.analytics.vertical import AnalyticsVerticalService


class AnalyticsVerticalResource(Resource):

    @security.http(
        login_required=True,
        params=RequestSchema(),
        response=ListAnalyticsVerticalResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, login_info, params):
        _result = AnalyticsVerticalService.get_list(params=params)
        return _result

    @security.http(
        login_required=True,
        form_data=AnalyticsVerticalRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def post(self, login_info, form_data):
        _id = AnalyticsVerticalService.create(form_data=form_data, login_info=login_info)
        return {
            '_id': str(_id)
        }

