from typing import List

from sqlalchemy import select
from db.models import City
from db.session import get_db
from sqlalchemy.orm import joinedload


class AllCityDAL:
    """Data Access Layer for operating cw info"""
    def __init__(self, db_session: get_db):
        self.db_session = db_session

    async def get_all_items(self) -> List[City]:
        query = await self.db_session.execute(
            select(City).options(joinedload(City.weather)))
        return query.scalars().all()
