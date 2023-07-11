# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.relevant_group import InputRelevantGroupRequestSchema
from services.admin.relevant_group import AdminRelevantGroupService


class AdminRelevantGroupByIdResource(Resource):

    @security.http(
        login_required=True,
        form_data=InputRelevantGroupRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, relevant_group_id, login_info, form_data):
        _result = AdminRelevantGroupService.update_by_id(relevant_group_id=relevant_group_id, login_info=login_info, form_data=form_data)
        return _result

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def delete(self, relevant_group_id, login_info):
        _result = AdminRelevantGroupService.delete_by_id(relevant_group_id=relevant_group_id, login_info=login_info)
        return _result

