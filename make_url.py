from city_geo import get_geo

BASE_URL = "https://api.openweathermap.org/"
API_KEY = "0101452058a9a7945c8b353b7f8d618f"


async def make_weather_url(city):
    geo_city = await get_geo(city)
    lat = geo_city["latitude"]
    lon = geo_city["longitude"]
    result = f"{BASE_URL}data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    return result
