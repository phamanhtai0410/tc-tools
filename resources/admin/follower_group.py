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
from schemas.follower_group import InputFollowerGroupRequestSchema, ListFollowerGroupResponseSchema
from schemas.request import RequestSchema
from services.admin.follower_group import AdminFollowerGroupService


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

        return _result

    @security.http(
        login_required=True,
        form_data=InputFollowerGroupRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info, form_data):
        _result = AdminFollowerGroupService.create(login_info=login_info, form_data=form_data)

        return _result
