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

class CheckResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    # def get(self, login_info):
    #    _result = AnalyticsVerticalService.get_account_profile_link()
    #    _result2 = AnalyticsVerticalService.get_keyword_url()
    #    merged_json = {**_result, **_result2}
    #    return merged_json 
    def post(self, login_info):
    #    _result = AnalyticsVerticalService.get_account_profile_link()
    #    _result2 = AnalyticsVerticalService.get_keyword_url()
    #    merged_json = {**_result, **_result2}
       AnalyticsVerticalService.update_favorite()
       return
      #  result = {'username': []}
      #  for json_obj in a:
      #    username = json_obj.get('username')
      #    if username is not None:
      #       result['username'].append(username)
    
    #    result_json = json.dumps(result)
        # a = AnalyticsVerticalService.getfavor()
        # result = {'username': []}
        # for json_obj in a:
        #  username = json_obj.get('username')
        #  if username is not None:
        #     result['username'].append(username)
        # print(result['username'])
        
        # return result['username']
       
    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def get(self,login_info):
         check_keyword = 'None'
         data = {
            "url": None,
            "type": 'None'
        }
         check_keyword=AnalyticsVerticalService.checkurl()
         if(check_keyword != 1):
            data['url'] = check_keyword
            data['type'] = 'Url'
            return data
         check_keyword = AnalyticsVerticalService.checkprofile()
         if(check_keyword != 2):
            data['url'] = check_keyword
            data['type'] = 'Profile'
            return data
         check_keyword =AnalyticsVerticalService.checkfolow()
         if(check_keyword!= 3):
            data['url'] = check_keyword
            data['type'] = 'folow'
            return data
         return data