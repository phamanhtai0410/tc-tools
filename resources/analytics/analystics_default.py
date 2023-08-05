# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from lib.enums.roles import Roles
from schemas.analytics.vertical import AnalyticsVerticalRequestSchema
from services.analytics.vertical import AnalyticsVerticalService


class AnalyticsDefault(Resource):
        @security.http(
        login_required=True,
        response=AnalyticsVerticalRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
        )
        def get(self, login_info):
               _id = AnalyticsVerticalService.get_list_default()
               return _id
        
        @security.http(
        login_required=True,
        form_data=AnalyticsVerticalRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
        )
        def put(self, form_data, login_info):
                AnalyticsVerticalService.edit(login_info=login_info, form_data=form_data)
                return {}
        
            
        




