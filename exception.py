# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""


class Sample(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 300
        self.msg = 'Sample'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'SAMPLE_ERROR'

    pass



