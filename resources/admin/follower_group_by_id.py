# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from lib.enums.roles import Roles
from schemas.follower_group import InputFollowerGroupRequestSchema
from services.admin.follower_group import AdminFollowerGroupService


class AdminFollowerGroupByIdResource(Resource):

    @security.http(
        login_required=True,
        form_data=InputFollowerGroupRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, follower_group_id, login_info, form_data):
        _result = AdminFollowerGroupService.update_by_id(
            follower_group_id=follower_group_id,
            login_info=login_info,
            form_data=form_data
        )
        return _result

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def delete(self, follower_group_id, login_info):
        _result = AdminFollowerGroupService.delete(
            follower_group_id=follower_group_id,
            login_info=login_info
        )
        return _result
