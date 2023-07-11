# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import os
from flask_restful import Resource, request
from flask import send_file, after_this_request

from connect import security
from lib.enums.roles import Roles
from schemas.analytics.vertcal_result import ListAnalyticsVerticalResultResponseSchema, RequestAnalyticsVerticalResultSchema
from schemas.request import RequestSchema
from services.analytics.vertical import AnalyticsVerticalService
from services.analytics.vertical_result import AnalyticsVerticalResultService


class AnalyticsVerticalResultExportResource(Resource):

    def get(self):
        params = request.args
        _result = AnalyticsVerticalResultService.export(params=params)

        @after_this_request
        def remove_file(response):
            print(response)
            os.remove(_result)
            return response

        return send_file(_result)
