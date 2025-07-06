# app/messages/schedule.py

from app.logs.log import setup_logger
from app.models.employee import Employee
from app.models.schedule import ScheduleBlock, ScheduleService

log = setup_logger()


class ScheduleCore:
    def __init__(
        self, message: str, sender_number: str, push_name: str, *args, **kwargs
    ):
        self.messsage = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.schedule = ScheduleService
        self.employee = Employee
        self.block = ScheduleBlock

    def add_schedule(self):
        try:
            stmt = ...

        except Exception as e:
            log.error(f"Error add schedule: {e}")
            return None

    def list_schedule(self): ...

    def delete_schedule(self): ...
