class AccountWatchNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = "Account watch's name existed"
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ACCOUNT_WATCH_NAME_EXISTED'

    pass
