from pydantic import BaseModel, Field
from pydantic.schema import datetime

class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class WeatherShema(TunedModel):
    id: int
    temp: int
    timestamp: datetime


class CityShema(TunedModel):
    id: int
    name: str
    latitude: float
    longitude: float
    country: str
    population: int
    is_capital: bool
    weather_id: int
    weather: WeatherShema
