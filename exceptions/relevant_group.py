class RelevantGroupNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'relevant group name existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_RELEVANT_GROUP_NAME_EXISTED'

    pass


class RelevantGroupNotFoundEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'relevant group not found'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_RELEVANT_GROUP_NOT_FOUND'

    pass
