import asyncio

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from city.prepare_weather_item import get_weather_items
from db.models import City, Weather
from db.session import get_db
from logger_config import cw_logger as logger
from settings import API_KEY, BASE_URL


async def get_url(lat, lon):
    url = f"{BASE_URL}data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    logger.debug(f"URL : {url}")
    return url


async def collect_weather():
    tasks = []
    old_weather = None

    db = get_db()
    session: AsyncSession = await anext(db)
    async with session.begin():
        selectable = select(City)
        cites = await session.execute(selectable)

        for city in cites.scalars():
            if city.weather_id:
                old_weather = city.weather_id
            url = await get_url(city.latitude, city.longitude)
            tasks.append(asyncio.create_task(get_weather_items(url, city, old_weather)))

        await session.flush()

        for task in tasks:
            weather_city = await task
            old_weather = weather_city[2]
            weather = weather_city[0]
            session.add(weather)
            await session.flush()

            city = weather_city[1]
            city.weather_id = weather.id
            session.add(city)
            if old_weather:
                logger.debug(f"Deleting weather с id: {old_weather}")
                del_weather = delete(Weather).where(Weather.id == old_weather)
                await session.execute(del_weather)

        await session.commit()
