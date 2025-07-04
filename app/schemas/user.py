# app/schemas/user.py

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    lastname: str
    phone: str

    class Config:
        orm_mode = True
