from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, desc
from app.models.habit import Habit
from app.models.completion import CompletionLog
from app.schemas.habit import HabitCreate, HabitUpdate
from uuid import UUID
from datetime import datetime, timedelta, date
import pytz

def get_today_in_tz(timezone_str: str) -> date:
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz).date()

async def get_user_habits(db: AsyncSession, user_id: UUID, timezone: str):
    result = await db.execute(select(Habit).where(and_(Habit.user_id == user_id, Habit.active == True)))
    habits = result.scalars().all()
    today = get_today_in_tz(timezone)
    
    response = []
    for habit in habits:
        comp_res = await db.execute(select(CompletionLog).where(and_(CompletionLog.habit_id == habit.id, CompletionLog.completed_date == today)))
        completed_today = comp_res.scalars().first() is not None
        habit.completed_today = completed_today
        response.append(habit)
    return response

async def create_habit(db: AsyncSession, user_id: UUID, habit: HabitCreate):
    db_habit = Habit(**habit.model_dump(), user_id=user_id)
    db.add(db_habit)
    await db.commit()
    await db.refresh(db_habit)
    return db_habit

async def get_habit(db: AsyncSession, habit_id: UUID):
    result = await db.execute(select(Habit).where(Habit.id == habit_id))
    return result.scalars().first()

async def update_habit(db: AsyncSession, db_habit: Habit, habit_update: HabitUpdate):
    for key, value in habit_update.model_dump().items():
        setattr(db_habit, key, value)
    await db.commit()
    await db.refresh(db_habit)
    return db_habit

async def delete_habit(db: AsyncSession, db_habit: Habit):
    db_habit.active = False
    await db.commit()
    return db_habit

async def log_completion(db: AsyncSession, habit_id: UUID, user_timezone: str):
    today = get_today_in_tz(user_timezone)
    existing = await db.execute(select(CompletionLog).where(and_(CompletionLog.habit_id == habit_id, CompletionLog.completed_date == today)))
    if existing.scalars().first():
        return None
    log = CompletionLog(habit_id=habit_id, completed_date=today)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def unlog_completion(db: AsyncSession, habit_id: UUID, user_timezone: str):
    today = get_today_in_tz(user_timezone)
    existing = await db.execute(select(CompletionLog).where(and_(CompletionLog.habit_id == habit_id, CompletionLog.completed_date == today)))
    log = existing.scalars().first()
    if log:
        await db.delete(log)
        await db.commit()
        return True
    return False

async def get_habit_history(db: AsyncSession, habit_id: UUID, start_date: date = None, end_date: date = None, timezone: str = "UTC"):
    if not end_date:
        end_date = get_today_in_tz(timezone)
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    result = await db.execute(
        select(CompletionLog).where(
            and_(
                CompletionLog.habit_id == habit_id,
                CompletionLog.completed_date >= start_date,
                CompletionLog.completed_date <= end_date
            )
        ).order_by(CompletionLog.completed_date.asc())
    )
    return result.scalars().all()
