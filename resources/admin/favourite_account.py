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
from schemas.favourite_account import InputFavouriteAccountRequestSchema
# from schemas.request import RequestSchema
from services.admin.favourite_account import AdminFavouriteAcccountService


class AdminFavouriteAccountResource(Resource):

    @security.http(
        login_required=True,
        form_data=InputFavouriteAccountRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info, form_data):
        _result = AdminFavouriteAcccountService.create_batch_of_accounts(login_info=login_info, form_data=form_data)
        return _result
    
    
