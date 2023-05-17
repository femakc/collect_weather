import asyncio

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from city.prepare_weather_item import get_weather_items
from db.models import City, Weather
from db.session import get_db
from logger_config import cw_logger as logger
from settings import API_KEY, BASE_URL


async def update_city(obj):
    db = get_db()
    session: AsyncSession = await anext(db)

    async with session.begin():
        one_weather = Weather(temp=obj["temp"], timestamp=obj["timestamp"])
        session.add(one_weather)
        return one_weather


async def one_city_weather(lat, lon):
    url = f"{BASE_URL}data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    logger.info(f"URL : {url}")
    weather_dict = await get_weather_items(url)
    return weather_dict


async def collect_weather():
    await asyncio.sleep(1)
    old_weather_list = []
    db = get_db()
    session: AsyncSession = await anext(db)
    async with session.begin():
        selectable = select(City)
        cites = await session.execute(selectable)

        for city in cites.scalars():

            if city.weather_id:
                old_weather_list.append(city.weather_id)
            obj = await one_city_weather(city.latitude, city.longitude)
            weather = await update_city(obj)
            city.weather_id = weather.id
            session.add(city)
            logger.debug(f"Create city with weather с id: {city.name}")

        if old_weather_list:
            logger.debug(f"Deleting weather с id: {old_weather_list}")
            del_weather = delete(Weather).where(Weather.id.in_(old_weather_list))
            await session.execute(del_weather)
        await session.commit()
