# app/models/schedule.py
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModels


class ScheduleBlock(BaseModels):
    __tablename__ = 'block'
    __table_args__ = {'schema': 'service'}

    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('employee.employees.id'), nullable=False
    )

    is_block: Mapped[bool] = mapped_column(
        Boolean, server_default=text('false'), nullable=False
    )
