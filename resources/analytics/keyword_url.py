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
from schemas.keyword_url import RemoveKeywordFormDataSchema, AddKeywordFormdataSchema



class KeywordURLResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def get(self, login_info):
        _result = AnalyticsVerticalService.get_keyword_url()
        print(_result)
        return _result
    
    @security.http(
        login_required=True,
        form_data=RemoveKeywordFormDataSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def delete(self, login_info,form_data):
        AnalyticsVerticalService.remove_key(form_data=form_data)

    @security.http(
        login_required=True,
        form_data=AddKeywordFormdataSchema(),

        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info,form_data):
        AnalyticsVerticalService.add_key(login_info=login_info,form_data=form_data)

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, login_info):
        AnalyticsVerticalService.is_used_false()    
        
        
