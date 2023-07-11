# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.analytics.vertical_logs import ListAnalyticsLogsResponseSchema
from schemas.request import RequestSchema
from services.analytics.vertical import AnalyticsVerticalService


class AnalyticsVerticalLogsResource(Resource):

    @security.http(
        login_required=True,
        params=RequestSchema(),
        response=ListAnalyticsLogsResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, login_info, params):
        _result = AnalyticsVerticalService.get_list_log(params=params)
        return _result

