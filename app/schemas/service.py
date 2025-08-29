from datetime import datetime

from pydantic import BaseModel


class ScheduleInEmployee(BaseModel):
    employee_id: int
    start_time: datetime
    end_time: datetime


class ScheduleEmployeeOut(BaseModel):
    message_id: str = 'schedule_deleted_successfully'
