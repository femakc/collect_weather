from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.shemas import CityShema
from db.dals import AllCityDAL
from db.session import get_db

cw_router = APIRouter()


@cw_router.get("/")
async def hello() -> str:
    return "Hello! This is collect weather service"


@cw_router.get("/get_weather", response_model=list[CityShema])
async def get_weather(db: AsyncSession = Depends(get_db)) -> list[Any]:
    async with db as session:
        async with session.begin():
            cw_dal = AllCityDAL(session)
            return await cw_dal.get_all_items()

