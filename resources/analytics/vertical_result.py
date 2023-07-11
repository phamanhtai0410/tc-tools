# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.analytics.vertcal_result import ListAnalyticsVerticalResultResponseSchema, RequestAnalyticsVerticalResultSchema
from schemas.request import RequestSchema
from services.analytics.vertical import AnalyticsVerticalService
from services.analytics.vertical_result import AnalyticsVerticalResultService


class AnalyticsVerticalResultResource(Resource):

    @security.http(
        login_required=True,
        params=RequestAnalyticsVerticalResultSchema(),
        response=ListAnalyticsVerticalResultResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, params, login_info):
        _result = AnalyticsVerticalResultService.get_list(params=params)
        return _result

