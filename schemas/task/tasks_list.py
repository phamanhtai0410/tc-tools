from marshmallow import Schema, EXCLUDE, fields, RAISE, validate
from lib import ObjectIdField, DatetimeField, TaskStatus, IsObjectId


class CrawlerTasksRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    page = fields.Integer(required=False, default=1, allow_none=True)
    page_size = fields.Integer(required=False, default=10, allow_none=True)
    vertical_id = fields.String(required=False, validate=IsObjectId(), allow_none=True)
    user_id = fields.String(required=False, validate=IsObjectId(), allow_none=True)
    search = fields.String(required=False, default=None, allow_none=True)
    sort = fields.String(required=False, validate=validate.OneOf([
        'desc',
        'asc'
    ]), allow_none=True)
    status = fields.String(required=False, validate=validate.OneOf([
        TaskStatus.PENDING,
        TaskStatus.PROCESSING,
        TaskStatus.DONE,
        TaskStatus.FAIL,
    ]), allow_none=True)
    start = fields.Float(required=False, default=0, allow_none=True)
    end = fields.Float(required=False, default=0, allow_none=True)


class CrawlerTasksSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    status = fields.String(required=True)
    vertical_id = ObjectIdField(required=True)
    user = fields.Dict(required=True)
    created_time = DatetimeField(required=True)


class CrawlerTasksResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    # {
    #     "items": result,
    #     'num_of_page': num_of_page,
    #     'page_size': page_size,
    #     'page': page
    # }
    items = fields.List(fields.Nested(CrawlerTasksSchema()), data_key='items', missing=[])
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)
