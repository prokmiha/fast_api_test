from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date

from db.models import Credit


class UserCreditsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_credits_by_user(self, user_id: int) -> list[Credit]:
        stmt = select(Credit).where(Credit.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_monthly_credits(self, until: date) -> list[Credit]:
        start_date = date(until.year, until.month, 1)
        stmt = select(Credit).where(Credit.issuance_date.between(start_date, until))
        result = await self.session.execute(stmt)
        return result.scalars().all()

