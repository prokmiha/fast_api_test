from pydantic import BaseModel
from typing import List


class PlanResponse(BaseModel):
    message: str

class PlanPerformanceItemIn(BaseModel):
    month: str
    category: str 
    plan_sum: float
    fact_sum: float
    completion: str

class PlanPerformanceItemOut(BaseModel):
    month: str
    category: str 
    plan_sum: float
    fact_sum: float
    completion: str

class PlanPerformanceResponse(BaseModel):
    performance_in: List[PlanPerformanceItemIn]
    performance_out: List[PlanPerformanceItemOut]

class YearPerformanceItem(BaseModel):
    month: str
    credit_count: int
    credit_plan_sum: float
    credit_sum: float
    credit_completion: float
    payment_count: int
    payment_plan_sum: float
    payment_sum: float
    payment_completion: float
    credit_year_percent: float
    payment_year_percent: float


class YearPerformanceResponse(BaseModel):
    performance: list[YearPerformanceItem]
