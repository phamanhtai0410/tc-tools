# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import DatetimeField
from lib.schema import ObjectIdField


class FollowerWatchSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    # _id = ObjectIdField()
    username = fields.String()
    total = fields.Integer()
    percent_1d = fields.Float()
    percent_3d = fields.Float()
    percent_7d = fields. Float()
    percent_30d = fields.Float()
    amount_1d = fields.Integer()
    amount_7d = fields.Integer()
    amount_30d = fields.Integer()
    is_new = fields.Bool()


class ListFollowerWatchResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(FollowerWatchSchema()), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
