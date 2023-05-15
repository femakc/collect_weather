from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import AllCityDAL
from db.models import City, Weather
from api.shemas import CityShema
from db.session import get_db

# from make_url import make_weather_url
# from collect_weather_service import get_temp

# app = FastAPI()
cw_router = APIRouter()


@cw_router.get("/")
async def hello() -> str:
    return "Hello!!!"


# @cw_router.get("/get_weather")
# async def get_weather(db: AsyncSession = Depends(get_db)) -> list[Any]:
#     async with db as session:
#         async with session.begin():
#             cw_dal = AllCityDAL(session)
#             return await cw_dal.get_all_items()
@cw_router.get("/get_weather", response_model=list[CityShema])
async def get_weather(db: AsyncSession = Depends(get_db)) -> list[Any]:
    async with db as session:
        async with session.begin():
            query = await session.execute(select(City).join(City.weather).where(Weather.id == City.weather_id))
        return query.scalars().all()
