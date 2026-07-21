from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = ""
    completed: bool = False
    due_date: Optional[date] = None

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value):
        if value and value < date.today():
            raise ValueError("due_date cannot be in the past")
        return value

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    due_date: date | None = None

    model_config = ConfigDict(from_attributes=True)

class TaskResponse(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)