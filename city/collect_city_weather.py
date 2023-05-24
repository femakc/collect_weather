import asyncio
from typing import Optional, Generator

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from city.prepare_weather_item import get_weather_items
from db.models import City, Weather
from db.session import get_db
from logger_config import cw_logger as logger
from settings import API_KEY, BASE_URL


async def get_url(lat, lon) -> str:
    url: str = f"{BASE_URL}data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    logger.debug("URL : %s", url)
    return url


async def collect_weather() -> None:
    tasks: list = []
    old_weather: Optional[int] = None

    db: Generator = get_db()
    session: AsyncSession = await anext(db)
    async with session.begin():
        selectable = select(City)
        cites = await session.execute(selectable)

        for city in cites.scalars():
            if city.weather_id:
                old_weather: int = city.weather_id
            url: str = await get_url(city.latitude, city.longitude)
            tasks.append(asyncio.create_task(get_weather_items(
                url, city, old_weather)))

        await session.flush()

        for task in tasks:
            weather_city: dict = await task
            logger.debug("weather_city : %s", weather_city)
            weather: Weather = weather_city["weather"]
            session.add(weather_city["weather"])
            await session.flush()

            city: City = weather_city["city"]
            city.weather_id = weather.id
            session.add(city)
            if weather_city["old_weather"]:
                logger.debug("Deleting weather с id: %d", old_weather)
                del_weather = delete(Weather).where(
                    Weather.id == weather_city["old_weather"])
                await session.execute(del_weather)

        await session.commit()
