# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, RAISE, EXCLUDE, fields


class AuthRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.String(required=True)
    password = fields.String(required=True)

class AuthResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    access_token = fields.String(required=True)