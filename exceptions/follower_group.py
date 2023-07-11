class FollowerGroupNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'Follower group name existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_FOLLOWER_GROUP_NAME_EXISTED'

    pass


class FollowerGroupNotExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'Follower group not existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_FOLLOWER_GROUP_NOT_EXISTED'

    pass
