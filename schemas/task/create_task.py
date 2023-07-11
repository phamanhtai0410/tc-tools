# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, RAISE, EXCLUDE, fields
from lib import IsObjectId


class CreateTaskRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    vertical_id = fields.String(required=True, validate=IsObjectId())
    title = fields.String(required=True)
    description = fields.String(required=False, missing='')


class CreateTaskResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    task_id = fields.String(required=True, validate=IsObjectId())
    status = fields.String(required=True)
