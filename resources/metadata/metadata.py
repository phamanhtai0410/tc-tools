# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource, request

from connect import security
from lib.enums.roles import Roles
from schemas.vertical import InputVerticalRequestSchema, ListVerticalResponseSchema
from schemas.request import RequestSchema
from services.admin.relevant_group import AdminRelevantGroupService
from services.admin.vertical import AdminVerticalService
from services.metadata.metadata import MetadataService


class MetadataResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN, Roles.USERS]
    )
    def get(self, login_info):
        _result = MetadataService.get()
        return _result
