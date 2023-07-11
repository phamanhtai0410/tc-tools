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
from schemas.follower_watch import ListFollowerWatchResponseSchema
from schemas.request import RequestSchema
from services.admin.follower_watch import AdminFollowerWatchService


class AdminFollowerWatchResource(Resource):

    @security.http(
        login_required=True,
        params=RequestSchema(),
        response=ListFollowerWatchResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, params, login_info):
        _ids = py_.get(request, 'args.ids', [])
        _result = AdminFollowerWatchService.get_list(params={
            **params,
            'ids': _ids
        })

        return _result

