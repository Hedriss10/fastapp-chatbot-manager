# app/schemas/employee.py

from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional


class EmployeeBase(BaseModel):
    username: str = Field(..., max_length=120)
    date_of_birth: str = Field(..., description="DD/MM/YYYY format")
    phone: str = Field(..., max_length=40)
    role: str = Field(..., max_length=40)
    password: str = Field(..., min_length=6, max_length=300)

    @validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        try:
            date_object = datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Invalid date format. Please use DD/MM/YYYY")
        if date_object.date() > datetime.now().date():
            raise ValueError("Date of birth cannot be in the future.")
        return value


class EmployeeOut(BaseModel):
    message_id: Optional[str] = "employee_created_successfully"


class EmployeeUpdate(BaseModel):
    username: Optional[str] = None
    date_of_birth: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None


class EmployeeUpdateOut(BaseModel):
    message_id: Optional[str] = "employee_updated_successfully"


class EmployeeDeleteOut(BaseModel):
    message_id: Optional[str] = "employee_deleted_successfully"
