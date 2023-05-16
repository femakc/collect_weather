import asyncio
import sys
from http import HTTPStatus

import requests
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from city.exceptions import EmptyResponseError, ResponseStatusCodeError
from db.models import City
from db.session import get_db
from logger_config import cw_logger as logger
from settings import X_API_KEY


async def collect_city_info():
    db = get_db()
    session: AsyncSession = await anext(db)
    f_url = "https://api.api-ninjas.com/v1/city?max_population=100000000&limit=50"
    headers = {'X-Api-Key': X_API_KEY}

    try:
        response = requests.get(f_url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            raise ResponseStatusCodeError()
        logger.info(f"response.status_code: {HTTPStatus.OK}")

        response_json: list[dict] = response.json()

        if not len(response_json):
            raise EmptyResponseError()

        inst_lst = [City(**dct) for dct in response_json]

    except Exception as error:
        logger.exception(error)
        sys.exit()

    async with session.begin():
        await session.execute(delete(City))
        session.add_all(inst_lst)
        await session.commit()


async def collect_city_info_second():
    await asyncio.sleep(1)
    db = get_db()
    session: AsyncSession = await anext(db)
    f_url = "https://api.api-ninjas.com/v1/city?max_population=10000000&limit=20"
    headers = {'X-Api-Key': X_API_KEY}

    try:
        response = requests.get(f_url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            raise ResponseStatusCodeError()
        logger.info(f"response.status_code: {HTTPStatus.OK}")

        response_json: list[dict] = response.json()

        if not len(response_json):
            raise EmptyResponseError()

        inst_lst = [City(**dct) for dct in response_json]

    except Exception as error:
        logger.exception(error)
        sys.exit()

    async with session.begin():
        session.add_all(inst_lst)
        await session.commit()
