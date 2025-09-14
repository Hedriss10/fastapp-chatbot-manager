from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class ScheduleInEmployee(BaseModel):
    employee_id: UUID
    start_time: datetime
    end_time: datetime


class ScheduleEmployeeOut(BaseModel):
    message_id: str = 'schedule_deleted_successfully'
