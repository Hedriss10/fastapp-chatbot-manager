# app/core/schedule.py

from sqlalchemy.orm import Session

from app.models.schedules.schedule import ScheduleService
from app.schemas.schedule import ScheduleInSchema
from app.schemas.pagination import PaginationParams


class ScheduleCore:
    
    def add_schedule(self, data: ScheduleInSchema, db: Session): ...
    
    
    def list_schedules(self,pagination: PaginationParams, db: Session): ...
    
    
    def get_schedule(self, id: int, user_id: int, db: Session): ...
    
    
    def update_schedule(self, id: int, data: ScheduleInSchema, db: Session): ...
    
    
    def delete_schedule(self, id: int, db: Session): ...
