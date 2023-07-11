# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import string
from datetime import timedelta

import jwt
import bcrypt
from pydash import get


from lib.logger import debug
from lib.enums.roles import Roles, RolesMethod


class MetadataService:

    @classmethod
    def get(cls):
        return {
            'roles': [
                {
                    'role': Roles.SUPER_ADMIN,
                    'access': [
                        {
                            'end_point': '/admin/users',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/admin/vertical_keyword_group',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/admin/global_setting',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/admin/follower_group',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/analytics/vertical/run',
                            'methods': [RolesMethod.READ, RolesMethod.CREATE]
                        },
                        {
                            'end_point': '/analytics/vertical/result',
                            'methods': [RolesMethod.READ]
                        },
                    ]
                },
                {
                    'role': Roles.ADMIN,
                    'access': [
                        {
                            'end_point': '/admin/users',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/admin/vertical_keyword_group',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/analytics/vertical',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/admin/global_setting',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/admin/follower_group',
                            'methods': [RolesMethod.CREATE, RolesMethod.READ, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/analytics/vertical/run',
                            'methods': [RolesMethod.READ, RolesMethod.CREATE]
                        },
                        {
                            'end_point': '/analytics/vertical/result',
                            'methods': [RolesMethod.READ]
                        },
                    ]
                },
                {
                    'role': Roles.USERS,
                    'access': [
                        {
                            'end_point': '/admin/vertical_keyword_group',
                            'methods': [RolesMethod.READ]
                        },
                        {
                            'end_point': '/analytics/vertical',
                            'methods': [RolesMethod.READ, RolesMethod.CREATE, RolesMethod.UPDATE, RolesMethod.DELETE]
                        },
                        {
                            'end_point': '/admin/global_setting',
                            'methods': [RolesMethod.READ]
                        },
                        {
                            'end_point': '/admin/follower_group',
                            'methods': [RolesMethod.READ]
                        },
                        {
                            'end_point': '/analytics/vertical/run',
                            'methods': [RolesMethod.READ, RolesMethod.CREATE]
                        },
                        {
                            'end_point': '/analytics/vertical/result',
                            'methods': [RolesMethod.READ]
                        },
                    ]
                }
            ]
        }
