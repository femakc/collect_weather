import sys

import aiohttp

from logger_config import cw_logger as logger
from settings import KELVIN_TO_CELSIUS


async def get_weather_items(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                html = await response.json()
                temp = int(html.get('main').get('temp') + KELVIN_TO_CELSIUS)
                timestamp = html.get('dt')
                weather_dict = {"temp": temp, "timestamp": timestamp}
        return weather_dict

    except Exception as error:
        logger.exception(error)
        sys.exit()
