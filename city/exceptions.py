class BaseParserException(Exception):
    message = 'Unknown collect error'

    def __str__(self) -> str:
        return self.message


class EmptyResponseError(BaseParserException):
    message = 'Server returned null value'


class ResponseStatusCodeError(BaseParserException):
    message = 'Unexpected response status code'


class ResponseCityApiError(BaseParserException):
    message = 'Bad Response from CityAPI'


class ResponseCityWeatherApiError(BaseParserException):
    message = 'Bad Response from WeatherAPI'


class UvicornError(BaseParserException):
    message = 'Uvicorn don`t start'