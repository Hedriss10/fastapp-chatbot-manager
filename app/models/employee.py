# app/models/employee.py

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

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
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


# class ScheduleEmployee(Base):
#     __tablename__ = 'schedule_employee'
#     __table_args__ = (
#         CheckConstraint(
#             "weekday IN ('segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo')",
#             name='schedule_employee_weekday_check',
#         ),
#         {'schema': 'time_recording'},
#     )

#     id: Mapped[int] = mapped_column(primary_key=True)

#     employee_id: Mapped[int] = mapped_column(
#         Integer,
#         ForeignKey('public.employee.id', ondelete='CASCADE'),
#         nullable=False,
#     )

#     weekday: Mapped[str] = mapped_column(String(9), nullable=False)

#     start_time: Mapped[datetime] = mapped_column(Time, nullable=False)
#     lunch_start: Mapped[datetime] = mapped_column(Time)
#     lunch_end: Mapped[datetime] = mapped_column(Time)
#     end_time: Mapped[datetime] = mapped_column(Time)

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')
#     )

#     updated_at: Mapped[datetime] = mapped_column(DateTime)
#     updated_by: Mapped[int] = mapped_column(Integer)
#     deleted_at: Mapped[datetime] = mapped_column(DateTime)
#     deleted_by: Mapped[int] = mapped_column(Integer)

#     is_deleted: Mapped[bool] = mapped_column(
#         Boolean, server_default=text('false'), nullable=False
#     )
