import aiohttp

from settings import KELVIN_TO_CELSIUS


async def get_weather_items(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            html = await response.json()
            temp = int(html.get('main').get('temp') + KELVIN_TO_CELSIUS)
            timestamp = html.get('dt')
            weather_dict = {"temp": temp, "timestamp": timestamp}
    return weather_dict
