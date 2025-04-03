from fastapi import APIRouter, Depends, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.plan import PlanResponse
from services.plan import PlanService
from db.session import get_session

router = APIRouter()

@router.post("/", response_model=PlanResponse, summary="Plans Upload")
async def plans_insert(new_plan: UploadFile = File(), session: AsyncSession = Depends(get_session)):
    return await PlanService(session).process_new_plan(new_plan)