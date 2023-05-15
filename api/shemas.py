from pydantic import BaseModel, Field


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class WeatherShema(TunedModel):
    id: int
    temp: int
    timestamp: int


class CityShema(TunedModel):
    id: int
    name: str
    latitude: float
    longitude: float
    country: str
    population: int
    is_capital: bool
    weather_id: int
    weather: WeatherShema = Field(None, alias='Weather')
    # weather: int

