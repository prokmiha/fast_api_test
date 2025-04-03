from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date

from db.models import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_payments_by_credit_id(self, credit_id: int) -> list[Payment]:
        stmt = select(Payment).where(Payment.credit_id == credit_id)
        result = await self.session.execute(stmt)
        
        return result.scalars().all()
    
    async def get_monthly_payments(self, until: date) -> list[Payment]:
        start_date = date(until.year, until.month, 1)
        
        stmt = select(Payment).where(Payment.payment_date.between(start_date, until))
        result = await self.session.execute(stmt)

        return result.scalars().all()


