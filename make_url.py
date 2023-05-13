from city_geo import get_geo
from settings import BASE_URL, API_KEY


async def make_weather_url(city):
    geo_city = await get_geo(city)
    lat = geo_city["latitude"]
    lon = geo_city["longitude"]
    result = f"{BASE_URL}data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    return result
