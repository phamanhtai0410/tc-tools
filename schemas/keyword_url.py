from marshmallow import EXCLUDE, Schema, fields
from lib import ObjectIdField
from lib import DatetimeField
from lib.schema import ObjectIdField


class KeywordURLRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    analytic_id = ObjectIdField(required=True, allow_none=False)

class RemoveKeywordFormDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    key_remove = fields.Str(required=True)
    

class AddKeywordFormdataSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    key_add = fields.Str(required=True)
