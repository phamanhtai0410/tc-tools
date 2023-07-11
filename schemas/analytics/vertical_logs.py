# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate, post_dump
from lib import DatetimeField
from lib.exception import BadRequest
from lib.schema import ObjectIdField, IsObjectId
from schemas.follower_group import FollowerGroupSchema
from schemas.vertical_keyword_group import VerticalKeywordGroupSchema

import pydash as py_

class RangeObjSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    start = fields.String()
    end = fields.String()

class RateObjSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    point = fields.String(required=True)
    quantity = fields.String(required=True)


class AnalyticsLogsSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    vertical_name = fields.String(required=True)
    follower_group_id = ObjectIdField(required=True, validate=IsObjectId())
    follower_group = fields.Nested(FollowerGroupSchema())
    vertical_keyword_groups = fields.List(ObjectIdField(), required=True, validate=validate.Length(min=1, max=1))
    vertical_keyword_groups_weight = fields.Float(required=True, allow_none=False, validate=validate.Range(min=0, max=100))
    recency_weight = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    engagement_weight = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    follower_quality_weight = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    account_verified_weight = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    end_date = DatetimeField(required=True)
    exclude_account = fields.List(fields.String, allow_none=True, default=[], missing=[])
    followers_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    following_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    tweet_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    listed_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    account_age_range = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    tweet_date = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    retweet_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    reply_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    like_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    quote_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    impression_count = fields.Nested(RangeObjSchema, required=False, allow_none=True, default=None)
    hashtags = fields.List(fields.String(), allow_none=True, default=[], missing=[])
    mentions = fields.List(fields.String(), allow_none=True, default=[], missing=[])
    cashtags = fields.List(fields.String(), allow_none=True, default=[], missing=[])
    annotations = fields.List(fields.String(), allow_none=True, default=[], missing=[])
    note = fields.String(required=False, default='', missing='')
    account_no_verified_point = fields.Float(required=False, allow_none=False, default=0)
    account_verified_point = fields.Float(required=False, allow_none=False, default=0)
    account_business_point = fields.Float(required=False, allow_none=False, default=0)
    note = fields.String(required=False, default='', missing='')
    vertical_keywords = fields.List(fields.Nested(VerticalKeywordGroupSchema))
    analytics_id = ObjectIdField()
    status = fields.String()

class ListAnalyticsLogsResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(AnalyticsLogsSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
    



