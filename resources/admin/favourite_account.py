# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request
import pydash as py_

from connect import security
from lib.enums.roles import Roles
from schemas.favourite_account import InputFavouriteAccountsRequestSchema,NoteFavouriteAccountRequestSchema,NoteFavouriteAccountResponseSchema
# from schemas.request import RequestSchema
from services.admin.favourite_account import AdminFavouriteAcccountService


class AdminFavouriteAccountResource(Resource):
    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, username, login_info):
        _result = AdminFavouriteAcccountService.create(login_info=login_info, username=username)
        return _result
    
    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def delete(self,login_info,username):
        _result = AdminFavouriteAcccountService.delete(login_info=login_info,username=username)
        return _result
    
    @security.http(
        login_required=True,
        form_data=NoteFavouriteAccountRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self,login_info,form_data,username):
        _result = AdminFavouriteAcccountService.put(login_info=login_info,form_data=form_data,username=username)
        return _result
    @security.http(
        login_required=True,
        response=NoteFavouriteAccountResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def get(self, username, login_info):
        _result = AdminFavouriteAcccountService.get(username=username)
        print(_result)
        return _result
    
    