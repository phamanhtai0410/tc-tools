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
from schemas.follower_group import InputFollowerGroupRequestSchema, ListFollowerGroupResponseSchema,InputOneFavouriteAccountRequestSchema
from schemas.request import RequestSchema
from services.admin.follower_group import AdminFollowerGroupService
from schemas.follower_group import RemoveFollowerGroupSchema, AddFollowerGroupSchema


class AdminFollowerGroupResource(Resource):

    @security.http(
        login_required=True,
        params=RequestSchema(),
        response=ListFollowerGroupResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, login_info, params):
        _ids = py_.get(request, 'args.ids', [])
        _result = AdminFollowerGroupService.get_list(params={
            **params,
            'ids': _ids
        })
        print(_result)
        return _result

    @security.http(
        login_required=True,
        form_data=InputFollowerGroupRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info, form_data):
        _result = AdminFollowerGroupService.create(login_info=login_info, form_data=form_data)
        return _result


    # @security.http(
    #     login_required=True,
    #     form_data=InputOneFavouriteAccountRequestSchema(),
    #     roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    # )
    # def delete(self, login_info, form_data):
    #     print("ok")
    #     _result = AdminFollowerGroupService.delete_by_name(login_info=login_info, form_data=form_data)
    #     return _result
    
    # @security.http(
    #     login_required=True,
    #     form_data=AddFollowerGroupSchema(),
    #     roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    # )
    # def put(self,login_info, form_data):
    #     AdminFollowerGroupService.add(form_data=form_data)
    
    # @security.http(
    #     login_required=True,
    #     form_data=RemoveFollowerGroupSchema(),
    #     roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    # )
    # def delete(self,login_info, form_data):
    #     AdminFollowerGroupService.remove(form_data=form_data)


        

