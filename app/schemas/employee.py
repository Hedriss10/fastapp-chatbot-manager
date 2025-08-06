# app/schemas/employee.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    username: str = Field(..., max_length=120)
    date_of_birth: datetime = Field(
        ..., description='Date of birth in DD/MM/YYYY format'
    )
    phone: str = Field(..., max_length=40)
    role: str = Field(
        default='Administrator',
        max_length=50,
        description='Role of the employee',
    )
    password: str = Field(..., min_length=6, max_length=300)


class EmployeeOut(BaseModel):
    message_id: Optional[str] = 'employee_created_successfully'


class EmployeeUpdate(BaseModel):
    username: Optional[str] = None
    date_of_birth: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None


class EmployeeUpdateOut(BaseModel):
    message_id: Optional[str] = 'employee_updated_successfully'


class EmployeeDeleteOut(BaseModel):
    message_id: Optional[str] = 'employee_deleted_successfully'


class EmployeeGetIdOut(BaseModel):
    id: int
    username: str
    date_of_birth: datetime
    phone: str
    role: str
