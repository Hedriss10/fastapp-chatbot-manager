# app/models/schedule.py

from datetime import datetime


from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ScheduleBlock(Base):
    __tablename__ = 'block'
    __table_args__ = {'schema': 'service'}

    id: Mapped[int] = mapped_column(primary_key=True)

    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('employee.employees.id'), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)

    is_block: Mapped[bool] = mapped_column(
        Boolean, server_default=text('false'), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, server_default=text('false'), nullable=False
    )
