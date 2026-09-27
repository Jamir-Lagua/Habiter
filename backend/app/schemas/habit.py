from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency_type: str
    frequency_days: Optional[List[int]] = None

class HabitCreate(HabitBase):
    pass

class HabitUpdate(HabitBase):
    active: bool

class HabitResponse(HabitBase):
    id: UUID
    user_id: UUID
    active: bool
    created_at: datetime
    completed_today: bool = False
    model_config = ConfigDict(from_attributes=True)
