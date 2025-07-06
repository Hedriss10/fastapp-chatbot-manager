# app/messages/employee.py

# TODO - criar o mecanismo da agenda
# TODO - criar a listagem de funcionarios

from app.logs.log import setup_logger
from app.models.employee import Employee

log = setup_logger()


class EmployeeCore:
    def __init__(self):
        self.employee = Employee

    def list_employee(self):
        try:
            stmt = ...

        except Exception as e:
            log.error(f"Logger: Error list employees{e}")
