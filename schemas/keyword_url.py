from marshmallow import EXCLUDE, Schema
from lib import ObjectIdField


class KeywordURLRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    analytic_id = ObjectIdField(required=True, allow_none=False)
