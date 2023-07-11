class FavouriteAccountNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = "Favourite Account's name existed"
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_FAVOURITE_ACCOUNT_NAME_EXISTED'

    pass
