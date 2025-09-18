# app/models/time_recording.py
import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModels


class ScheduleEmployee(BaseModels):
    __tablename__ = 'schedule_employee'
    __table_args__ = (
        CheckConstraint(
            (
                'weekday IN ('
                "'segunda', "
                "'terça', "
                "'quarta', "
                "'quinta', "
                "'sexta', "
                "'sábado', "
                "'domingo'"
                ')'
            ),
            name='schedule_employee_weekday_check',
        ),
        {
            'schema': 'time_recording',
            'extend_existing': True,
        },
    )

    employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('employee.employees.id', ondelete='CASCADE'),
        nullable=False,
    )

    weekday: Mapped[str] = mapped_column(String(9), nullable=False)

    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    lunch_start: Mapped[datetime.time] = mapped_column(Time)
    lunch_end: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)
