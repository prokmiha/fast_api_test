from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date

from db.models import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_payments_by_credit_id(self, credit_id: int) -> list[Payment]:
        stmt = select(Payment).where(Payment.credit_id == credit_id)
        result = await self.session.execute(stmt)
        
        return result.scalars().all()
    
    async def get_monthly_payments(self, until: date) -> float:
        start_date = date(until.year, until.month, 1)
        
        stmt = select(
            func.sum(Payment.sum)).where( 
            Payment.payment_date.between(start_date, until),
            Payment.type_id.in_([1, 2]))
            
        result = await self.session.execute(stmt)

        return result.scalar() or 0
    
    async def get_yearly_payments(self, until: date) -> list[Payment]:
        stmt = (
            select(
                func.month(Payment.payment_date).label("month"),
                func.count(Payment.id).label("payment_count"),
                func.sum(Payment.sum).label("payment_total"),
                Payment.type_id
            )
            .where(func.extract("year", Payment.payment_date) == until)
            .group_by(func.month(Payment.payment_date), Payment.type_id)
            .order_by("month")
        )
        result = await self.session.execute(stmt)
        return result.all()


