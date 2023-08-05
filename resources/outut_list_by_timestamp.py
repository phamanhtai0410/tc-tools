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

class OutputListByTimestampResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def get(self,login_info,timestamp):
        _output_list = OutputListService.get_output_list(login_info=login_info,timestamp=timestamp)
        return _output_list

