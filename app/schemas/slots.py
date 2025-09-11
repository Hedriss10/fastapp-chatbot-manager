from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class SlotsInSchema(BaseModel):
    employee_id: int
    work_start: str
    work_end: str
    slot_minutes: int = 30
    target_date: Optional[date] = None


class SlotSchema(BaseModel):
    start: datetime
    end: datetime
