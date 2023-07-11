class UsernameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'Username already exists.'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_USERNAME_EXISTED'

    pass

class CanOnlyAddUserWithLessRolesEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'can only add user with less roles'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_CAN_ONLY_ADD_USER_WITH_LESS_ROLES'
        