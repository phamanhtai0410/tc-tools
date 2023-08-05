class AccountNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = "Account's name existed"
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ACCOUNT_NAME_EXISTED'

    pass

class AccountNameNotExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = "Account's name didn't exist"
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ACCOUNT_NAME_NOT_EXISTED'

    pass
