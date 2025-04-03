from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from schemas.user_credit import UserCreditsResponse, ClosedCredit, OpenCredit
from repository.user_credit import UserCreditsRepository
from repository.payment import PaymentRepository


class UserCreditService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.TYPE_BODY = 1
        self.TYPE_PERCENT = 2

    async def get_user_credits(self, user_id: int) -> UserCreditsResponse:
        today = date.today()
        credits = await UserCreditsRepository(self.session).get_credits_by_user(user_id)

        closed = []
        open_ = []

        for credit in credits:
            payments = await PaymentRepository(self.session).get_payments_by_credit_id(credit.id)
            paid_body = sum(p.sum for p in payments if p.type_id == self.TYPE_BODY)
            paid_percent = sum(p.sum for p in payments if p.type_id == self.TYPE_PERCENT)

            if credit.actual_return_date:
                closed.append(ClosedCredit(
                    is_closed=True,
                    issuance_date=credit.issuance_date,
                    actual_return_date=credit.actual_return_date,
                    body=credit.body,
                    percent=credit.percent,
                    total_payments=paid_body + paid_percent
                ))
            else:
                overdue_days = max((today - credit.return_date).days, 0)
                open_.append(OpenCredit(
                    is_closed=False,
                    issuance_date=credit.issuance_date,
                    return_date=credit.return_date,
                    overdue_days=overdue_days,
                    body=credit.body,
                    percent=credit.percent,
                    paid_body=paid_body,
                    paid_percent=paid_percent,
                ))
        
        return UserCreditsResponse(closed=closed, open=open_)