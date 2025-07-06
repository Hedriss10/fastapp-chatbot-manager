# app/models/schedule.py

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base


class ScheduleService(Base):
    __tablename__ = "schedule_service"
    __table_args__ = {"schema": "shedule.service"}

    id: Mapped[int] = mapped_column(primary_key=True)
    time_register: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_check: Mapped[int] = mapped_column(Boolean, nullable=False)
    is_awayalone: Mapped[int] = mapped_column(Boolean, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"""{self.id} created successfully"""


class ScheduleBlock(Base):
    __tablename__ = "block"
    __table_args__ = {"schema": "schedule"}

    id: Mapped[int] = mapped_column(primary_key=True)

    star_time: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    end_time: Mapped[datetime.datetime | None] = mapped_column(DateTime)

    employee_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("public.employee.id")
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )

    updated_at: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    updated_by: Mapped[int | None] = mapped_column(Integer)
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime)
    deleted_by: Mapped[int | None] = mapped_column(Integer)

    is_block: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), nullable=False
    )
