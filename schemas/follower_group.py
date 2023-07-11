# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import DatetimeField
from lib.schema import ObjectIdField


class InputFollowerGroupRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.String(required=True)
    accounts = fields.List(fields.String, required=True, validate=validate.Length(min=1))


class FollowerGroupSchema(InputFollowerGroupRequestSchema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    name = fields.String()
    accounts = fields.List(fields.String)
    updated_time = DatetimeField()
    updated_by = fields.String()


class ListFollowerGroupResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(FollowerGroupSchema()), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
