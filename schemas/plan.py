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
