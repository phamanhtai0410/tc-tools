class VerticalNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'vertical name existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_VERTICAL_NAME_EXISTED'

    pass


class VerticalNotFoundEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'vertical not found existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_VERTICAL_NOT_FOUND'

    pass


class AnalyticsVerticalKeywordGroupCanNotDuplicateEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'vertical not found existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ANALYTICS_VERTICAL_KEYWORD_GROUP_CAN_NOT_DUPLICATE'

    pass


class AnalyticsNotFoundEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'analytics not found'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ANALYTICS_NOT_FOUND'

    pass


class AnalyticsVerticalNameExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'analytics vertical name existed'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ANALYTICS_VERTICAL_NAME'

    pass


class AccountFilteredDetailNotExistedEx(Exception):
    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = 'Account filtered detail not existed.'
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_ACCOUNT_FILTERED_DETAIL_NOT_EXISTED.'

    pass
