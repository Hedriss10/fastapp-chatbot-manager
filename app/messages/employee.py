# app/messages/employee.py

# TODO - criar o mecanismo da agenda
# TODO - criar a listagem de funcionarios

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.logs.log import setup_logger
from app.models.employee import Employee
from app.models.messages import SummaryMessage

log = setup_logger()


LIST_EMPLOYEE = "select_barber"


class EmployeeCore:
    def __init__(self, db: Session):
        self.db = db
        self.employee = Employee
        self.message_summary = SummaryMessage

    def list_employee(self):
        try:
            employees = select(
                self.employee.id,
                self.employee.username,
            ).where(
                ~self.employee.is_deleted
            )
            
            result_employees = self.db.execute(employees).fetchall()
            
            message_summary = select(
                self.message_summary.id,
                self.message_summary.ticket,
                self.message_summary.message
            ).where(
                self.message_summary == LIST_EMPLOYEE
            )
            
            list_employee = self.db.execute(message_summary).fetchone()
            
            for l in list_employee:
                l.format("")
            

        except Exception as e:
            log.error(f"Logger: Error list employees{e}")
