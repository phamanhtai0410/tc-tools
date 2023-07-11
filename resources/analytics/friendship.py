# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from lib.enums.roles import Roles
from schemas.analytics.friendship import AccountFriendShipRequestSchema
from services.analytics.vertical_result import AnalyticsVerticalResultService


class AccountFriendShipResource(Resource):

    @security.http(
        login_required=True,
        form_data=AccountFriendShipRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info, form_data):
        _followers_you_follow = get(form_data, 'followers_you_follow', [])
        _account = get(form_data, 'account')
        _result = AnalyticsVerticalResultService.insert_account_friendship(
            account=_account,
            followers_you_follow=_followers_you_follow
        )
        return {
            '_id': str(_result)
        }
