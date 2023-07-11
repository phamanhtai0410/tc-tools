class VerticalKeywordGroupNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'vertical keyword group name existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_VERTICAL_KEYWORD_GROUP_NAME_EXISTED'

    pass


class VerticalKeywordGroupNotExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'vertical keyword group not existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_VERTICAL_KEYWORD_GROUP_NOT_EXISTED'

    pass


class KeywordURLNotExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'Keyword URL not existed or used.'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_KEYWORD_URL_NOT_EXISTED_OR_USED'

    pass


class AccountProfileLinkNotExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'Account profile link not existed or used.'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ACCOUNT_PROFILE_LINK_NOT_EXISTED_OR_USED'

    pass
