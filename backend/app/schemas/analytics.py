from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import List

class DailyCompletion(BaseModel):
    date: date
    completed: bool

class HabitSummary(BaseModel):
    habit_id: UUID
    habit_name: str
    current_streak: int
    longest_streak: int
    completion_rate_7d: float
    completion_rate_30d: float
    completion_rate_all_time: float
    completions: List[DailyCompletion]
