# from pydantic import BaseModel
#
#
# class TunedModel(BaseModel):
#     class Config:
#         """tells pydantic to convert even non dict obj to json"""
#
#         orm_mode = True
#
#
# class GeoCity(TunedModel):
#     id: int
#     name: str
#     latitude: float
#     longitude: float
#     country: str
#     population: int
#     is_capital: bool
#
#
# class WeatherCity(TunedModel):
#     id: int
