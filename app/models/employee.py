# app/models/employee.py
import uuid
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.log import setup_logger
from app.db.base import Base

log = setup_logger()


EMPLOYEE_FIELDS = [
    'username',
    'date_of_birth',
    'phone',
    'role',
]

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'employee'}

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    role: Mapped[str] = mapped_column(String(40), nullable=False)
    session_token: Mapped[str] = mapped_column(Text, nullable=True)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"""{self.username} created employee_successfully"""
