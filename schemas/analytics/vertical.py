# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import math
import datetime

from marshmallow import Schema, EXCLUDE, fields, validate, post_dump
from lib import DatetimeField, dt_utcnow
from lib.exception import BadRequest
from lib.schema import ObjectIdField, IsObjectId, NotBlank

import pydash as py_
from schemas.follower_group import FollowerGroupSchema

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

class AnalyticsVerticalRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    vertical_name = fields.String(required=False)
    follower_group_id = ObjectIdField(required=True, validate=IsObjectId())
    vertical_keyword_groups = fields.List(ObjectIdField(), required=True, validate=validate.Length(min=1, max=1))
    vertical_keyword_groups_weight = fields.Float(required=True, allow_none=False)
    recency_weight = fields.Float(required=True)
    follower_quality_weight = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    account_verified_weight = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    end_date = DatetimeField(required=False)
    exclude_account = fields.List(fields.String,required = False, allow_none=True, default=[], missing=[])
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
    hashtags = fields.List(fields.String(validate=NotBlank()), allow_none=True, default=[], missing=[])
    mentions = fields.List(fields.String(validate=NotBlank()), allow_none=True, default=[], missing=[])
    cashtags = fields.List(fields.String(validate=NotBlank()), allow_none=True, default=[], missing=[])
    annotations = fields.List(fields.String(validate=NotBlank()), allow_none=True, default=[], missing=[])
    note = fields.String(required=False, default='', missing='')
    account_no_verified_point = fields.Float(required=False, allow_none=False, default=1)
    account_verified_point = fields.Float(required=False, allow_none=False, default=2)
    account_business_point = fields.Float(required=False, allow_none=False, default=4)
    auto = fields.Bool(required=False, allow_none=False, default=1)


    @post_dump(pass_many=True)
    def post_dump_analytics_vertical(self, data, **kwargs):
        _error_obj = {}
        _vertical_keyword_groups_weight = py_.get(data, 'vertical_keyword_groups_weight')
        _recency_weight = py_.get(data, 'recency_weight')
        _follower_quality_weight = py_.get(data, 'follower_quality_weight')
        _account_verified_weight = py_.get(data, 'account_verified_weight')

        if sum([_vertical_keyword_groups_weight, _recency_weight, _follower_quality_weight, _account_verified_weight]) != 100:
            py_.set_(_error_obj, "vertical_keyword_groups_weight", [
                "Total weight must be 100"
            ])
            py_.set_(_error_obj, "recency_weight", [
                "Total weight must be 100"
            ])
            py_.set_(_error_obj, "follower_quality_weight", [
                "Total weight must be 100"
            ])
            py_.set_(_error_obj, "account_verified_weight", [
                "Total weight must be 100"
            ])

        # _end_date = py_.get(data, 'end_date')
        # if  abs((_end_date - dt_utcnow()).days) > 7:
        #     py_.set_(_error_obj, 'end_date', [
        #         "The end_date field must be within a 7-day"
        #     ])

        if _error_obj:
            raise BadRequest(msg="Invalid params", errors=[_error_obj])

        return data



    # @post_dump(pass_many=True)
    # def post_dump_analytics_vertical(self, data, **kwargs):
    #     _error_obj = {}
    #     if data['followers_count'] and not data['followers_count_rate']:
    #         py_.set_(_error_obj, "followers_count_rate", [
    #             "Missing data for required field."
    #         ])
        
    #     if data['following_count'] and not data['following_count_rate']:
    #         py_.set_(_error_obj, "following_count_rate", [
    #             "Missing data for required field."
    #         ])

    #     if data['tweet_count'] and not data['tweet_count_rate']:
    #         py_.set_(_error_obj, "tweet_count_rate", [
    #             "Missing data for required field."
    #         ])

    #     if data['listed_count'] and not data['listed_count_rate']:
    #         py_.set_(_error_obj, "listed_count_rate", [
    #             "Missing data for required field."
    #         ])

    #     if data['retweet_count'] and not data['retweet_count_rate']:
    #         py_.set_(_error_obj, "retweet_count_rate", [
    #             "Missing data for required field."
    #         ])

    #     if data['like_count'] and not data['like_count_rate']:
    #         py_.set_(_error_obj, "like_count_rate", [
    #             "Missing data for required field."
    #         ])

    #     if data['quote_count'] and not data['quote_count_rate']:
    #         py_.set_(_error_obj, "quote_count_rate", [
    #             "Missing data for required field."
    #         ])

    #     if data['impression_count'] and not data['impression_count_rate']:
    #         py_.set_(_error_obj, "impression_count_rate", [
    #             "Missing data for required field."
    #         ])
        
    #     if data['hashtags'] and not data['hashtags_point']:
    #         py_.set_(_error_obj, "hashtags_point", [
    #             "Missing data for required field."
    #         ])

    #     if data['mentions'] and not data['mentions_point']:
    #         py_.set_(_error_obj, "mentions_point", [
    #             "Missing data for required field."
    #         ])

    #     if data['cashtags'] and not data['cashtags_point']:
    #         py_.set_(_error_obj, "cashtags_point", [
    #             "Missing data for required field."
    #         ])

    #     if data['annotations'] and not data['annotations_point']:
    #         py_.set_(_error_obj, "annotations_point", [
    #             "Missing data for required field."
    #         ])
        
    #     if data['analyst_account'] and (not data['follower_quality_score'] or not data['follower_quality_weight']):
    #         py_.set_(_error_obj, "follower_quality_score", [
    #             "Missing data for required field."
    #         ])
    #         py_.set_(_error_obj, "follower_quality_weight", [
    #             "Missing data for required field."
    #         ])

    #     if data['tweet_date'] and py_.get(data, 'tweet_date.end') and not py_.get(data, 'tweet_date.start'):
    #         py_.set_(_error_obj, "tweet_date", {
    #             "start": [
    #                 "Missing data for required field."
    #             ]
    #         })

    #     if data['account_age_range'] and py_.get(data, 'account_age_range.end') and not py_.get(data, 'account_age_range.start'):
    #         py_.set_(_error_obj, "account_age_range", {
    #             "start": [
    #                 "Missing data for required field."
    #             ]
    #         })
        
    #     print( py_.get(data, 'exclude_account', None))
    #     if py_.get(data, 'exclude_account', None) is None:
    #         data['exclude_account'] = []

    #     if py_.get(data, 'analyst_account', None) is None:
    #         data['analyst_account'] = []

    #     if _error_obj:
    #         raise BadRequest(msg="Invalid params", errors=[_error_obj])

    #     return data

class AnalyticsVerticalSchema(AnalyticsVerticalRequestSchema):

    _id = ObjectIdField()
    vertical_keywords = fields.List(fields.Nested(VerticalKeywordGroupSchema))
    vertical_name = fields.String()
    follower_group = fields.Nested(FollowerGroupSchema())
    status = fields.String()

class ListAnalyticsVerticalResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(AnalyticsVerticalSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()
    



