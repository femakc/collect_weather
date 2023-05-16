class BaseParserException(Exception):
    message = 'Unknown collect error'

    def __str__(self) -> str:
        return self.message


class EmptyResponseError(BaseParserException):
    message = 'Server returned null value'


class ResponseStatusCodeError(BaseParserException):
    message = 'Unexpected response status code'
