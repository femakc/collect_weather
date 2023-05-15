from typing import List
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import City, Weather
from api.shemas import CityShema


class AllCityDAL:
    """Data Access Layer for operating cw info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_items(self) -> List[City]:

        query = await self.db_session.execute(
            select(City)
            .order_by(City.id))

        # query = await self.db_session.execute(City, Weather)
        # # records = query.all()
        # # for  in records:
        # # weather = await self.db_session.execute(select(Weather))
        # # parent, child = db.query(Parent, Child).join(Child, Parent.child == Child.cid)

        return query.scalars().all()
