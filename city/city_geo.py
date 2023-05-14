import sys
from http import HTTPStatus
from typing import Optional

import aiohttp
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update

from api.handlers import get_weather
from collect_weather_service import get_temp
from db.models import City, Weather
from db.session import get_db
# from make_url import make_weather_url
from settings import X_API_KEY, BASE_URL, API_KEY
from exceptions import EmptyResponseError, ResponseStatusCodeError
from logger_config import cw_logger as logger


# BASE_URL = "https://api.openweathermap.org/"
# API_KEY = "0101452058a9a7945c8b353b7f8d618f"
# X_API_KEY = "hgwMzL0zKdvwe2cljulQ9g==ToLekCxPkDwwFoON"


async def update_city(obj):
    db = get_db()
    session: AsyncSession = await anext(db)
    # one_city = select(City).where(City.id == city_id)

    async with session.begin():
        one_weather = Weather(temp=obj["temp"], timestamp=obj["timestamp"])
        session.add(one_weather)
        return one_weather



async def one_city_weather(city, lat, lon):
    url = f"{BASE_URL}data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    weather_dict = await get_temp(url)
    return weather_dict


async def collect_weather():
    db = get_db()
    session: AsyncSession = await anext(db)
    async with session.begin():
        selectable = select(City)

        cites = await session.execute(selectable)

        for city in cites.scalars():
            print(city.weather)
            obj = await one_city_weather(city.name, city.latitude, city.longitude)
            weather = await update_city(obj)
            city.weather = weather.id
            session.add(city)
        await session.commit()


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
