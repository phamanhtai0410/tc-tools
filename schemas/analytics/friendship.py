from marshmallow import EXCLUDE, Schema, fields


class AccountFriendShipRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    account = fields.String(required=True, allow_none=False)
    followers_you_follow = fields.List(fields.String, required=True, allow_none=False)
