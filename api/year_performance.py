from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from schemas.plan import YearPerformanceResponse
from services.plan import YearPerformance
from db.session import get_session

router = APIRouter()

@router.get("/{raw_year}", response_model=YearPerformanceResponse, summary="Year Performance")
async def plan_performance(raw_year: str, session: AsyncSession = Depends(get_session)):
    target_year = YearPerformance(session).validate_year(raw_year)

    return await YearPerformance(session).process_year_performance(target_year)