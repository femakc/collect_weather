import sys
from http import HTTPStatus
from typing import Optional

import aiohttp
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from db.models import City
from db.session import get_db
from settings import X_API_KEY
from exceptions import EmptyResponseError, ResponseStatusCodeError
from logger_config import cw_logger as logger


# BASE_URL = "https://api.openweathermap.org/"
# API_KEY = "0101452058a9a7945c8b353b7f8d618f"
# X_API_KEY = "hgwMzL0zKdvwe2cljulQ9g==ToLekCxPkDwwFoON"


async def collect_city_info():
    db = get_db()
    session: AsyncSession = await anext(db)
    f_url = "https://api.api-ninjas.com/v1/city?max_population=100000000&limit=50"
    headers = {'X-Api-Key': X_API_KEY}

    try:
        response = requests.get(f_url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            raise ResponseStatusCodeError()

        response_json: list[dict] = response.json()

        if not len(response_json):
            raise EmptyResponseError()

        inst_lst = [City(**dct) for dct in response_json]
        # logger.info(
        #     f"Вот что мы собрали: {inst_lst}"
        # )
    except Exception as error:
        logger.exception(error)
        sys.exit()

    async with session.begin():
        await session.execute(delete(City))
        session.add_all(inst_lst)
        await session.commit()


async def get_geo(city):
    url = f"https://api.api-ninjas.com/v1/city?name={city}"
    headers = {'X-Api-Key': X_API_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False, headers=headers) as response:
            html = await response.json()
    return html[0]
