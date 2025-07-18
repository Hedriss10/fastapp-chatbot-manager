# app/schemas/login.py
from pydantic import BaseModel


class LoginUser(BaseModel):
    phone: str
    
class LoginEmployee(BaseModel):
    phone: str
    password: str
    

class LoginUserOut(BaseModel):
    message_id: str = "user_logged_successfully"
    access_token: str = None

    
class LoginEmployeeOut(BaseModel):
    message_id: str = "employee_logged_successfully"
    access_token: str = None