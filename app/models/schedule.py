# app/models/schedule.py

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base as db


class ScheduleService(db.Model):
    __tablename__ = "schedule_service"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(primary_key=True)
    time_register: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(db.Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(db.Integer, nullable=True)
    product_id: Mapped[int] = mapped_column(db.Integer, nullable=False)
    employee_id: Mapped[int] = mapped_column(db.Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, nullable=False)
    is_check: Mapped[int] = mapped_column(db.Boolean, nullable=False)
    is_awayalone: Mapped[int] = mapped_column(db.Boolean, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(db.Boolean, default=False)

    def __repr__(self):
        return f"""{self.id} created successfully"""
