from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from schemas.plan import PlanPerformanceResponse
from services.plan import PlanPerformance
from db.session import get_session

router = APIRouter()

@router.get("/{raw_date}", response_model=PlanPerformanceResponse, summary="Plan Performance")
async def plan_performance(raw_date: str, session: AsyncSession = Depends(get_session)):
    try:
        target_date = PlanPerformance(session).validate_date(raw_date)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Error: Correct date format DD.MM.YYYY"
        )

    return await PlanPerformance(session).process_plan_performance(target_date)