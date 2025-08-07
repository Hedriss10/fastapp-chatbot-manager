# app/models/schedule.py

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger


class ScheduleBlock(Base):
    __tablename__ = 'block'
    __table_args__ = {'schema': 'service'}

    id: Mapped[int] = mapped_column(primary_key=True)

    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('employee.employees.id')
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text('now()')
    )

    updated_at: Mapped[datetime] = mapped_column(DateTime)
    updated_by: Mapped[int] = mapped_column(Integer)
    deleted_at: Mapped[datetime] = mapped_column(DateTime)
    deleted_by: Mapped[int] = mapped_column(Integer)

    is_block: Mapped[bool] = mapped_column(
        Boolean, server_default=text('false'), nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean, server_default=text('false'), nullable=False
    )