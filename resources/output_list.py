# -*- coding: utf-8 -*-
"""
   Description:
        -
     -
"""
from flask_restful import Resource

from connect import security
from services.output_list import OutputListService
# from schemas.score import InputTopScoreRequestSchema, ListTopScoreResponseSchema
from lib.enums.roles import Roles
import pydash as py_

class OutputListResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self,login_info):
        OutputListService.get_top_score(login_info)
        OutputListService.output_to_favor(login_info)
        return {}


