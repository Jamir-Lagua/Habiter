from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date, datetime

class CompletionLogResponse(BaseModel):
    id: UUID
    habit_id: UUID
    completed_date: date
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
