# app/core/employee.py
from sqlalchemy.orm import Session

from app.models.employee.employee import Employee
from app.schemas.employee import EmployeeUpdate
from app.schemas.pagination import PaginationParams


class EmployeeCore:
    def __init__(self, db: Session):
        self.db = db

    def get_employee(self, id: int):
        return Employee.get_employee(id, self.db)

    def add_employee(self, data: Employee):
        return Employee.add_employee(data, self.db)

    def list_employees(self, pagination: PaginationParams):
        return Employee.list_employees(pagination, self.db)

    def update_employee(self, id: int, data: EmployeeUpdate):
        return Employee.update_employee(id, data, self.db)

    def delete_employee(self, id: int):
        return Employee.delete_employee(id, self.db)
