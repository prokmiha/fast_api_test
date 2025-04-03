from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from datetime import date

from db.models import Credit


class UserCreditsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_credits_by_user(self, user_id: int) -> list[Credit]:
        stmt = select(Credit).where(Credit.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_monthly_credits(self, until: date) -> float:
        start_date = date(until.year, until.month, 1)
        stmt = select(
            func.sum(Credit.body)).where(
            Credit.issuance_date.between(start_date, until))
        result = await self.session.execute(stmt)
        
        return result.scalar() or 0
    
    async def get_yearly_credits(self, year: int):
        stmt = (
            select(
                func.month(Credit.issuance_date).label("month"),
                func.count(Credit.id).label("credit_count"),
                func.sum(Credit.body).label("credit_total")
            )
            .where(extract("year", Credit.issuance_date) == year)
            .group_by(func.month(Credit.issuance_date))
            .order_by("month")
        )
        result = await self.session.execute(stmt)
        return result.all()


