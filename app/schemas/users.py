# app/schemas/user.py
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    lastname: str
    phone: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    lastname: Optional[str] = None
    phone: Optional[str] = None


class UserOut(BaseModel):
    id: UUID
    username: str
    lastname: str
    phone: str
    message_id: Optional[str] = 'user_created_successfully'


class UserUpdateOut(BaseModel):
    message_id: Optional[str] = 'user_updated_successfully'


class UserDeleteOut(BaseModel):
    message_id: Optional[str] = 'user_deleted_successfully'
