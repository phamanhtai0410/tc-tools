from marshmallow import EXCLUDE, Schema, fields
from lib import ObjectIdField


class AccountsFilteredRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    analytic_id = ObjectIdField(required=True, allow_none=False)
    account_names = fields.List(fields.String, required=True, allow_none=False)


class AccountsFilteredNote(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    username = fields.String(required=True, allow_none=False)
    note = fields.String(required=False, allow_none=True)
class AccountFilteredDetailRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    username = fields.String(required=True, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    verified = fields.Bool(required=False, allow_none=True)
    verified_type = fields.String(required=False, allow_none=True)
    join = fields.String(required=False, allow_none=True)
    followers = fields.String(required=False, allow_none=True)
    following = fields.String(required=False, allow_none=True)
    tweet_count = fields.String(required=False, allow_none=True)
    user_url = fields.String(required=False, allow_none=True)
    user_location = fields.String(required=False, allow_none=True)
    user_professional_category = fields.String(required=False, allow_none=True)
    note = fields.String(required=False, allow_none=True)
