from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, func
from datetime import date

from db.models import Plan

class PlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def plan_exists(self, period, category_id) -> bool:
        stmt = select(Plan).where(Plan.period == period, Plan.category_id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def add_plan(self, plan: Plan):
        self.session.add(plan)

    async def get_current_plan(self, target_date: date) -> list[Plan]:
        target_period = date(target_date.year, target_date.month, 1)
        stmt = select(Plan).where(Plan.period == target_period)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def get_yearly_plans(self, year: int):
        stmt = (
            select(
                func.month(Plan.period).label("month"),
                func.sum(Plan.total_sum).label("plan_sum"),
                Plan.category_id
            )
            .where(extract("year", Plan.period) == year)
            .group_by(func.month(Plan.period), Plan.category_id)
            .order_by("month")
        )
        result = await self.session.execute(stmt)
        return result.all()

