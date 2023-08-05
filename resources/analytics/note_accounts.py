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
from schemas.analytics.accounts_filtered import AccountsFilteredRequestSchema, AccountFilteredDetailRequestSchema, AccountsFilteredNote
from services.analytics.vertical_result import AnalyticsVerticalResultService

class AccountsNote(Resource):
    @security.http(
        login_required=True,
        form_data=AccountsFilteredNote(),
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def put(self, login_info, form_data):
        note = get(form_data, 'note')
        username = get(form_data,'username')
        AnalyticsVerticalResultService.add_note(
            note=note,username = username
        )
        return {}

   

