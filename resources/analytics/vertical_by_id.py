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


class AnalyticsVerticalByIdResource(Resource):

    @security.http(
        login_required=True,
        form_data=AnalyticsVerticalRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def put(self, analytics_vertical_id, form_data, login_info):
        AnalyticsVerticalService.update_by_id(analytics_vertical_id=analytics_vertical_id, login_info=login_info, form_data=form_data)
        return {}

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def delete(self, analytics_vertical_id, login_info):
        AnalyticsVerticalService.delete(analytics_vertical_id=analytics_vertical_id, login_info=login_info)
        return {}

