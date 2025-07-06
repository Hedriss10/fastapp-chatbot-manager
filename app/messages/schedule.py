# app/messages/schedule.py

from app.models.employee import Employee
from app.models.schedule import ScheduleService


class ScheduleCore:
    def __init__(
        self, message: str, sender_number: str, push_name: str, *args, **kwargs
    ):
        self.messsage = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.schedule = ScheduleService
        self.employee = Employee

    def add_schedule(self): ...

    def list_schedule(self): ...

    def delete_schedule(self): ...
