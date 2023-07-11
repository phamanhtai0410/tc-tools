from datetime import datetime

from bson import ObjectId
from pydash import get

from lib import TaskStatus, dt_utcnow
from models import CrawlerTasksModel


class CrawlerTaskServices:
    @classmethod
    def create_task(cls, user_id: str, vertical_id: str, title: str, description: str):
        # Check user permission

        # Insert DB
        _inserted = CrawlerTasksModel.insert_one({
            'title': title,
            'description': description,
            'vertical_id': ObjectId(vertical_id),
            'user_id': ObjectId(user_id),
            'status': TaskStatus.PENDING,
            'created_time': dt_utcnow(),
            'created_by': 'CrawlerTaskServices:create_task',
            'updated_time': dt_utcnow(),
            'updated_by': '',
        })

        return {
            'task_id': get(_inserted, '_id'),
            'status': TaskStatus.PENDING
        }

    @classmethod
    def tasks_list(
        cls,
        page: int,
        page_size: int,
        vertical_id: str,
        user_id: str,
        search: str,
        status: str,
        sort: str,
        start: float,
        end: float
    ):
        _filter = {}

        if vertical_id != 'all':
            _filter['vertical_id'] = ObjectId(vertical_id)
        if user_id != 'all':
            _filter['user_id'] = ObjectId(user_id)
        if status != 'all':
            _filter['status'] = status

        if search is not None:
            _filter['$or'] = [
                {
                    "title": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "description": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]

        if start:
            _filter['created_time'] = {
                '$gte': datetime.utcfromtimestamp(start)
            }
            if end:
                _filter['created_time']['$lte'] = datetime.utcfromtimestamp(end)

        _offset = page > 0 and (page - 1) * page_size or 0

        _pipeline = [
            {
                '$match': _filter
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'user_id',
                    'foreignField': '_id',
                    'as': 'user',
                }
            },
            {
                '$unwind': '$user'
            },
            {
                "$sort": {
                    "created_time": sort
                }
            },
            {
                '$skip': _offset
            },
            {
                '$limit': page_size
            }
        ]

        _items = CrawlerTasksModel.col.aggregate(pipeline=_pipeline)

        _items = list(_items)

        # print(_items)

        _num_of_page = (len(_items) / page_size)
        if (len(_items) % page_size) > 0:
            _num_of_page = _num_of_page + 1

        # return {
        #     'items': _items,
        #     'page': page,
        #     'page_size': page_size,
        #     'num_of_page': _num_of_page
        # }

        return {
                'items': [
                    {
                        '_id': '64705dc77ecc7defd81012d3',
                        'title': 'Mockup',
                        'description': 'Mockup des',
                        'vertical_id': '64705dc77ecc7defd8191ec3',
                        'user': {
                            '_id': '64705dc77ecc7defd8101ec3',
                            'name': 'admin'
                        },
                        'status': 'PENDING',
                        'created_time': '2023-05-26T14:20:36.219+07:00'
                    }
                ],
                'page': 1,
                'page_size': 2,
                'num_of_page': 1
        }
