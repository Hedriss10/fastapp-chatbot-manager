# app/schemas/user.py

from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    lastname: str
    phone: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    lastname: str
    phone: str
    message_id: Optional[str] = "user_created_successfully"


class UserUpdateOut(BaseModel):
    message_id: Optional[str] = "user_updated_successfully"


class UserDeleteOut(BaseModel):
    message_id: Optional[str] = "user_deleted_successfully"
