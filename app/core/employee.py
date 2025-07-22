# app/core/employee.py

from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.pagination import PaginationParams
from app.schemas.employee import EmployeeUpdate
from app.schemas.employee import (
    EmployeeBase,
    EmployeeUpdateOut,
    EmployeeDeleteOut,
    EmployeeOut,
    EmployeeUpdate,
)


class EmployeeCore:
    @staticmethod
    def add_employee(data: Employee, db: Session):
        return Employee.add_employee(data, db)

    @staticmethod
    def list_employees(pagination: PaginationParams, db: Session):
        return Employee.list_employees(pagination, db)

    @staticmethod
    def update_employee(id: int, data: EmployeeUpdate, db: Session):
        return Employee.update_employee(id, data, db)

    @staticmethod
    def delete_employee(id: int, db: Session):
        return Employee.delete_employee(id, db)
