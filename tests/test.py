import unittest

from city.prepare_weather_item import get_weather_items
from db.models import Weather
from settings import BASE_URL, API_KEY

LAT = 35.6897
LON = 139.692


class TestCollector(unittest.TestCase):
    """Testing collect func"""
    async def test_get_weather_items(self):
        url = f"{BASE_URL}data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}"
        city_id = 100
        old_weather = None
        item = await get_weather_items(
            url,
            city_id,
            old_weather)
        self.assertEqual(item, dict(), " Alarm!!")
        self.assertEqual(item.get("weather"), str, " Alarm!!")

