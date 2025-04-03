from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_credit import UserCreditsResponse
from services.user_credit import UserCreditService
from db.session import get_session

router = APIRouter()

@router.get("/{user_id}", response_model=UserCreditsResponse, summary="Кредити користувача")
async def user_credits(user_id: int, session: AsyncSession = Depends(get_session)):
    return await UserCreditService(session).get_user_credits(user_id)