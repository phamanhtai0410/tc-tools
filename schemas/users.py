# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate
from lib import DatetimeField
from lib.schema import ObjectIdField
from lib.enums.roles import Roles


class CreateUserRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Regexp(regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', flags=0, error='Password contains letters and number characters'), validate.Length(min=8, error='Password should be greater than length 8')])
    name = fields.String(required=True, validate=validate.Length(min=1))
    role = fields.String(required=True, validate=validate.OneOf([
        Roles.SUPER_ADMIN,
        Roles.ADMIN,
        Roles.USERS
    ]))

class UpdateUserPasswordRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=False, validate=validate.Length(min=1))
    password = fields.String(required=False, allow_none=True, validate=[validate.Regexp(regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', flags=0, error='Password contains letters and number characters'), validate.Length(min=8, error='Password should be greater than length 8')])
    role = fields.String(required=False, validate=validate.OneOf([
        Roles.ADMIN,
        Roles.USERS
    ]), allow_none=True)

class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    username = fields.String(required=True)
    name = fields.String(required=True)
    roles = fields.List(fields.String(), default=[], missing=[])
    created_time = DatetimeField()
    created_by = fields.String()

class ListUserResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(UserSchema), default=[], missing=[])
    page = fields.Integer()
    page_size = fields.Integer()
    num_of_page = fields.Integer()