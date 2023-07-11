# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import DatetimeField
from lib.schema import ObjectIdField
from schemas.request import RequestSchema

class InputRelevantGroupRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    name = fields.String(required=True)
    weight = fields.Float(required=True)
    note = fields.String(required=False)

class RelevantGroupSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    name = fields.String(required=True)
    weight = fields.Float(required=True)
    note = fields.String(required=False)
    created_time = DatetimeField()
    created_by = fields.String()
    updated_time = DatetimeField()
    updated_by = fields.String()

class ListRelevantGroupResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(RelevantGroupSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
