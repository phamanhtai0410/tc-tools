# -*- coding: utf-8 -*-
"""
   Description:
        -
     -
"""
from flask_restful import Resource
from connect import security
from services.ip_logger import IpLoggerService
from lib.enums.roles import Roles
import pydash as py_

class IpLoggerResource(Resource):

    @security.http(
        login_required=True,
        roles=[Roles.ADMIN, Roles.SUPER_ADMIN]
    )
    def post(self,login_info):
        IpLoggerService.check_ip()
        return {}