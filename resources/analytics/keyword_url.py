# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from lib.enums.roles import Roles
from services.analytics.vertical import AnalyticsVerticalService


class KeywordURLResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def get(self, login_info):
        _result = AnalyticsVerticalService.get_keyword_url()
        return _result
