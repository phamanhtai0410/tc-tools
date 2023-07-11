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


class AnalyticsVerticalRunResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def post(self, analytics_vertical_id, login_info):
        AnalyticsVerticalService.run(analytics_vertical_id=analytics_vertical_id, login_info=login_info)
        return {}

