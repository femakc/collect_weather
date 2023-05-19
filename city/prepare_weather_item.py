import sys
from typing import Any, Optional

import aiohttp

from city.exceptions import ResponseStatusCodeError
from db.models import Weather
from logger_config import cw_logger as logger
from settings import KELVIN_TO_CELSIUS


async def get_weather_items(url: str, city_id: int, old_weather: Optional[int]) -> list:
    add_list: list = []
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, ssl=False) as r:
                if r.status != 200:
                    logger.error("response: %s", r)
                    raise ResponseStatusCodeError()
                response: Any = await r.json()
                temp: int = int(response.get('main').get('temp') + KELVIN_TO_CELSIUS)
                timestamp: Optional[str] = response.get('dt')
                add_list.append(Weather(temp=temp, timestamp=timestamp))
                add_list.append(city_id)
                add_list.append(old_weather)

    except Exception as error:
        logger.exception(error)
        sys.exit()

    return add_list
