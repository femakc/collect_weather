import sys

import aiohttp
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from city.exceptions import EmptyResponseError
from db.models import City
from db.session import get_db
from logger_config import cw_logger as logger
from settings import X_API_KEY


async def collect_city_info():
    headers = {'X-Api-Key': X_API_KEY}
    url_list = [
        "https://api.api-ninjas.com/v1/city?max_population=100000000&limit=25",
        "https://api.api-ninjas.com/v1/city?max_population=10000000&limit=25"
    ]
    for url in url_list:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, headers=headers, ssl=False) as r:
                    response = await r.json()
                    response += response

        except Exception as error:
            logger.exception(error)
            sys.exit()

    logger.info(f"response: {response}")

    response_json: list[dict] = response

    if not len(response_json):
        raise EmptyResponseError()
    inst_lst = [City(**dct) for dct in response_json]

    db = get_db()
    session: AsyncSession = await anext(db)
    async with session.begin():
        await session.execute(delete(City))
        session.add_all(inst_lst)
        await session.commit()
