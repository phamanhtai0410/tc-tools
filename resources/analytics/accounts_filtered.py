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
from schemas.analytics.accounts_filtered import AccountsFilteredRequestSchema, AccountFilteredDetailRequestSchema
from services.analytics.vertical_result import AnalyticsVerticalResultService


class AccountsFilteredResource(Resource):

    @security.http(
        login_required=True,
        form_data=AccountsFilteredRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self, login_info, form_data):
        _usernames = get(form_data, 'account_names', [])
        _analytic_id = get(form_data, 'analytic_id')
        _result = AnalyticsVerticalResultService.insert_accounts_filtered(
            analytic_id=_analytic_id,
            usernames=_usernames
        )
        return {
            '_id': str(_result)
        }

    @security.http(
        login_required=True,
        form_data=AccountFilteredDetailRequestSchema(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, login_info, form_data):
        _username = get(form_data, 'username')
        _name = get(form_data, 'name')
        _description = get(form_data, 'description')
        _verified = get(form_data, 'verified')
        _verified_type = get(form_data, 'verified_type')
        _join = get(form_data, 'join')
        _followers = get(form_data, 'followers')
        _following = get(form_data, 'following')
        _tweet_count = get(form_data, 'tweet_count')
        _user_url = get(form_data, 'user_url')
        _user_location = get(form_data, 'user_location')
        _user_professional_category = get(form_data, 'user_professional_category')

        _result = AnalyticsVerticalResultService.update_account_filtered_detail(
            username=_username,
            name=_name,
            description=_description,
            verified=_verified,
            verified_type=_verified_type,
            join=_join,
            followers=_followers,
            following=_following,
            tweet_count=_tweet_count,
            user_url=_user_url,
            user_location=_user_location,
            user_professional_category=_user_professional_category
        )
        return {
            '_id': str(_result)
        }
