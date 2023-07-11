# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import DatetimeField
from lib.schema import ObjectIdField


class InputTopScoreRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    from_time = fields.Integer()


# class TopScoreItemSchema(Schema):
#     class Meta:
#         unknown = EXCLUDE
#         ordered = True

#     _id = ObjectIdField()
#     username = fields.String()
#     keyword_in_description = fields.Integer()
#     number_of_frendship = fields.Integer()
#     url = fields.Str()
    
class ListTopScoreResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Dict())
    status = fields.Str()
