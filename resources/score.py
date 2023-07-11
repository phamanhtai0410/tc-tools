# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from services.score import ScoreService
from schemas.score import InputTopScoreRequestSchema, ListTopScoreResponseSchema
from lib.enums.roles import Roles
from pydash import get

class ScoreResource(Resource):

    @security.http(
        login_required=False,
        params=InputTopScoreRequestSchema(),
        response=ListTopScoreResponseSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def get(self, params):
        _from_time = get(params, 'from_time')
        print(
            'Resource - from time = ', _from_time
        )
        _top_score = ScoreService.get_top_score(from_time=_from_time)
        return _top_score
