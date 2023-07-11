# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import DatetimeField
from lib.schema import ObjectIdField

class InputVerticalKeywordGroupRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.String(required=True)
    keywords = fields.List(fields.String, required=True, validate=validate.Length(min=1))

class VerticalKeywordGroupSchema(InputVerticalKeywordGroupRequestSchema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    updated_time = DatetimeField()
    updated_by = fields.String()

class ListVerticalKeywordGroupResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(VerticalKeywordGroupSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()