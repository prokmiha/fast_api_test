from datetime import date

from pydantic import BaseModel


class ClosedCredit(BaseModel):
    is_closed: bool
    issuance_date: date
    actual_return_date: date
    body: float
    percent: float
    total_payments: float

    class Config:
        json_encoder = {
            date: lambda date_format: date_format.strftime('%d.%m.%Y'),
        }


class OpenCredit(BaseModel):
    is_closed: bool
    issuance_date: date
    return_date: date
    overdue_days: int
    body: float
    percent: float
    paid_body: float
    paid_percent: float

    class Config:
        json_encoder = {
            date: lambda date_format: date_format.strftime('%d.%m.%Y'),
        }


class UserCreditsResponse(BaseModel):
    closed: list[ClosedCredit]
    open: list[OpenCredit]
