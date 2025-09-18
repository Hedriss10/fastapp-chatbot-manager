from datetime import date
from sqlalchemy import (
    Date,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModels


class Employee(BaseModels):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'employee'}

    username: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    role: Mapped[str] = mapped_column(String(40), nullable=False)
    session_token: Mapped[str] = mapped_column(Text, nullable=True)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
