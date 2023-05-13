from typing import List

from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
from session import get_db
from db.models import City


class AllCityDAL:
    """Data Access Layer for operating cw info"""
    def __init__(self, db_session: get_db):
        self.db_session = db_session

    async def get_all_items(self) -> List[City]:
        query = await self.db_session.execute(
            select(City).order_by(City.id)
        )
        return query.scalars().all()
