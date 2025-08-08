# app/core/schedule.py

from sqlalchemy.orm import Session

from app.models.schedules.schedule import ScheduleService
from app.schemas.schedule import ScheduleInSchema
from app.schemas.pagination import PaginationParams


class ScheduleCore:
    @staticmethod
    def add_schedule(data: ScheduleInSchema, db: Session): ...
    
    @staticmethod
    def list_schedules(pagination: PaginationParams, db: Session): ...
    
    @staticmethod
    def get_schedule(id: int, db: Session): ...
    
    @staticmethod
    def update_schedule(id: int, data: ScheduleInSchema, db: Session): ...
    
    @staticmethod
    def delete_schedule(id: int, db: Session): ...
