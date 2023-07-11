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

import pydash as py_

from schemas.request import RequestSchema

class RequestAnalyticsVerticalResultSchema(RequestSchema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    analytic_log_id = ObjectIdField(required=True)


class PublicMetricsObjSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    followers_count = fields.Float(default=0, missing=0)
    following_count = fields.Float(default=0, missing=0)
    tweet_count = fields.Float(default=0, missing=0)
    listed_count = fields.Float(default=0, missing=0)


class AnalyticsVerticalResultSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    analytic_log_id = ObjectIdField()
    verified = fields.Boolean(default=False, missing=False)
    username = fields.String(required=True)
    public_metrics = fields.Nested(PublicMetricsObjSchema, default={}, missing={})
    created_at = fields.Integer()
    description = fields.String(default='', missing='')
    name = fields.String(default='', missing='')
    id = fields.String(required=True)
    # keyword_in_description = fields.Float(default=0, missing=0)
    verify_score = fields.Float(default=0, missing=0)
    engagement_score = fields.Float(default=0, missing=0)
    keyword_relevance_score = fields.Float(default=0, missing=0)
    followers_quality_score = fields.Float(default=0, missing=0)
    recency_score = fields.Float(default=0, missing=0)
    total_score = fields.Float(default=0, missing=0)


class ListAnalyticsVerticalResultResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(AnalyticsVerticalResultSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
    



