# app/schemas/schedule.py

from datetime import datetime

from pydantic import BaseModel, field_validator


class ScheduleInSchema(BaseModel):
    product_id: int
    employee_id: int
    user_id: int
    time_register: datetime

    @field_validator('time_register', mode='after')
    def parse_time(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d %H:%M')
        return value


class ScheduleOutSchema(BaseModel):
    message_id: str = 'schedule_created_successfully'


class UpdateScheduleInSchema(BaseModel):
    product_id: int
    employee_id: int
    user_id: int
    time_register: datetime


class UpdateScheduleOutSchema(BaseModel):
    message_id: str = 'schedule_updated_successfully'


class DeleteScheduleOutSchema(BaseModel):
    message_id: str = 'schedule_deleted_successfully'


class CheckScheduleOutSchema(BaseModel):
    is_check: bool
