from http import HTTPStatus


class YaCutError(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InvalidAPIUsage(YaCutError):
    status_code = HTTPStatus.BAD_REQUEST


class ShortIDNotFound(YaCutError):
    status_code = HTTPStatus.NOT_FOUND
