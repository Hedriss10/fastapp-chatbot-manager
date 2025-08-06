# app/schemas/login.py
from typing import Any, Dict, Optional

from pydantic import BaseModel


class LoginUser(BaseModel):
    phone: str


class LoginEmployee(BaseModel):
    phone: str
    password: str


class LoginUserOut(BaseModel):
    message_id: str = 'user_logged_successfully'
    user: Optional[Dict[str, Any]] = None
    access_token: Optional[str] = None


class LoginEmployeeOut(BaseModel):
    message_id: str = 'employee_logged_successfully'
    user: Optional[Dict[str, Any]] = None
    access_token: Optional[str] = None
