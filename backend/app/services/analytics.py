from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.habit import Habit
from app.models.completion import CompletionLog
from app.schemas.analytics import HabitSummary, DailyCompletion
from uuid import UUID
from datetime import datetime, timedelta
import pytz

def get_today_in_tz(timezone_str: str):
    tz = pytz.timezone(timezone_str)
    return datetime.now(tz).date()

async def get_habit_analytics(db: AsyncSession, user_id: UUID, timezone: str):
    habits_res = await db.execute(select(Habit).where(and_(Habit.user_id == user_id, Habit.active == True)))
    habits = habits_res.scalars().all()
    
    today = get_today_in_tz(timezone)
    summaries = []
    
    for habit in habits:
        logs_res = await db.execute(select(CompletionLog).where(CompletionLog.habit_id == habit.id).order_by(CompletionLog.completed_date.asc()))
        logs = logs_res.scalars().all()
        dates_set = {log.completed_date for log in logs}
        
        # Calculate longest streak
        longest_streak = 0
        current = 0
        prev_date = None
        for log in logs:
            if prev_date is None:
                current = 1
            else:
                if (log.completed_date - prev_date).days == 1:
                    current += 1
                else:
                    current = 1
            if current > longest_streak:
                longest_streak = current
            prev_date = log.completed_date
            
        # Calculate current streak
        current_streak = 0
        check_date = today
        if today not in dates_set:
            check_date = today - timedelta(days=1)
        
        while check_date in dates_set:
            current_streak += 1
            check_date -= timedelta(days=1)
            
        # Calculate completions for last 30 days
        completions_list = []
        for i in range(29, -1, -1):
            d = today - timedelta(days=i)
            completions_list.append(DailyCompletion(date=d, completed=d in dates_set))
            
        # Rates
        c7 = sum(1 for c in completions_list[-7:] if c.completed)
        rate7 = (c7 / 7.0) * 100
        c30 = sum(1 for c in completions_list if c.completed)
        rate30 = (c30 / 30.0) * 100
        
        all_time_rate = 0.0
        days_since_creation = (today - habit.created_at.date()).days + 1
        if days_since_creation > 0:
            all_time_rate = (len(logs) / float(days_since_creation)) * 100
            
        summaries.append(HabitSummary(
            habit_id=habit.id,
            habit_name=habit.name,
            current_streak=current_streak,
            longest_streak=longest_streak,
            completion_rate_7d=rate7,
            completion_rate_30d=rate30,
            completion_rate_all_time=all_time_rate,
            completions=completions_list
        ))
        
    return summaries
