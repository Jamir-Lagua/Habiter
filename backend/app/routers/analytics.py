from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.analytics import HabitSummary
from app.dependencies import get_current_user
from app.models.user import User
from app.services.analytics import get_habit_analytics
from typing import List

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary", response_model=List[HabitSummary])
async def get_analytics_summary(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_habit_analytics(db, current_user.id, current_user.timezone)
