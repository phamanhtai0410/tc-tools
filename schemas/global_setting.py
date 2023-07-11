import math

from marshmallow import Schema, EXCLUDE, fields, validate, post_dump
from config import Config
from lib import DatetimeField
from lib.exception import BadRequest
from lib.schema import ObjectIdField, IsObjectId

import pydash as py_

from schemas.vertical_keyword_group import VerticalKeywordGroupSchema

class RangeObjSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    start = fields.String(allow_none=True)
    end = fields.String(allow_none=True)

    @post_dump(pass_many=True)
    def post_dump_range(self, data, **kwargs):
        _start = py_.get(data, 'start')
        _end = py_.get(data, 'end')
        try:
            if (_start and not _start.isnumeric()) or (_end and not _end.isnumeric()) or (_start == "" or _end == ""):
                raise Exception('Invalid params')

            return data
        except:
            raise BadRequest(msg="Invalid params", errors=[{
                'start': [
                    'must be a string number'
                ],
                'end': [
                    'must be a string number'
                ]
            }])


class RateObjSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    point = fields.String(required=True)
    quantity = fields.String(required=True)

class InputGlobalSettingRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    followers_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    following_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    tweet_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    listed_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    account_age_range = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    tweet_date = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    retweet_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    reply_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    like_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    quote_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    impression_count = fields.Nested(RangeObjSchema, required=True, allow_none=False, default=1)
    account_no_verified_point = fields.Float(required=True, allow_none=False, default=1)
    account_verified_point = fields.Float(required=True, allow_none=False, default=1)
    account_business_point = fields.Float(required=True, allow_none=False, default=1)

class GlobalSettingSchema(InputGlobalSettingRequestSchema):

    _id = ObjectIdField()
    key = fields.String(required=True, default=Config.DEFAULT_GLOBAL_SETTING_KEY)

class ListGlobalSettingResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(GlobalSettingSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
    