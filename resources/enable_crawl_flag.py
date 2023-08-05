# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
import json
from connect import security
from lib.enums.roles import Roles
from services.analytics.vertical import AnalyticsVerticalService

class EnableCrawlFlagResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info):
       AnalyticsVerticalService.update_favorite()
       return {}
    
  
            
    
       
       
       
