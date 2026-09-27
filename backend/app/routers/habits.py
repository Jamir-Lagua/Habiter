from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse
from app.schemas.completion import CompletionLogResponse
from app.dependencies import get_current_user
from app.models.user import User
from app.services.habits import (
    get_user_habits, create_habit, get_habit, update_habit, delete_habit,
    log_completion, unlog_completion, get_habit_history
)
from uuid import UUID
from typing import List
from datetime import date
from pydantic import RootModel

router = APIRouter(prefix="/habits", tags=["habits"])

@router.get("/", response_model=List[HabitResponse])
async def list_habits(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    habits = await get_user_habits(db, current_user.id, current_user.timezone)
    return habits

@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_new_habit(habit: HabitCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await create_habit(db, current_user.id, habit)

async def get_and_check_habit(habit_id: UUID, db: AsyncSession, user_id: UUID):
    habit = await get_habit(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this habit")
    return habit

@router.put("/{habit_id}", response_model=HabitResponse)
async def update_existing_habit(habit_id: UUID, habit_update: HabitUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = await get_and_check_habit(habit_id, db, current_user.id)
    return await update_habit(db, habit, habit_update)

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_habit(habit_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = await get_and_check_habit(habit_id, db, current_user.id)
    await delete_habit(db, habit)

@router.post("/{habit_id}/complete", response_model=CompletionLogResponse)
async def complete_habit(habit_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = await get_and_check_habit(habit_id, db, current_user.id)
    log = await log_completion(db, habit.id, current_user.timezone)
    if not log:
        raise HTTPException(status_code=409, detail="Habit already completed today")
    return log

@router.delete("/{habit_id}/complete", status_code=status.HTTP_204_NO_CONTENT)
async def uncomplete_habit(habit_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = await get_and_check_habit(habit_id, db, current_user.id)
    success = await unlog_completion(db, habit.id, current_user.timezone)
    if not success:
        raise HTTPException(status_code=404, detail="No completion found for today")

@router.get("/{habit_id}/history", response_model=List[CompletionLogResponse])
async def habit_history(habit_id: UUID, start_date: date = None, end_date: date = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    habit = await get_and_check_habit(habit_id, db, current_user.id)
    logs = await get_habit_history(db, habit.id, start_date, end_date, current_user.timezone)
    return logs
