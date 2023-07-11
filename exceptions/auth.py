class UsernameOrPasswordNotCorrectEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'username or password not correct'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USERNAME_OR_PASSWORD_NOT_CORRECT'

    pass
