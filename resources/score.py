# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from services.score import ScoreService
from services.ip_logger import IpLoggerService
from schemas.score import InputTopScoreRequestSchema, ListTopScoreResponseSchema
from lib.enums.roles import Roles

class ScoreResource(Resource):
    @security.http(
        login_required=False,
        # params=InputTopScoreRequestSchema(),
        response=ListTopScoreResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def get(self):
        _top_score = ScoreService.get_top_score()
        return _top_score
