# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import DatetimeField
from lib.schema import ObjectIdField, IsObjectId

class KeywordObjSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    keyword = fields.String(required=True)
    relevant_group_id = ObjectIdField(required=True, validate=IsObjectId())
    is_twitter_key = fields.Boolean(required=True)
    is_account_key = fields.Boolean(required=True)

class InputVerticalRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.String(required=True)
    keywords = fields.List(fields.Nested((KeywordObjSchema)), required=True)

class VerticalSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    name = fields.String(required=True)
    keywords = fields.List(fields.Nested((KeywordObjSchema)), default=[], missing=[])

class ListVerticalResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(VerticalSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()