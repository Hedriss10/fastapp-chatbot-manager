# app/models/time_recording.py
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ScheduleEmployee(Base):
    __tablename__ = 'schedule_employee'
    __table_args__ = (
        CheckConstraint(
            "weekday IN ('segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo')",
            name='schedule_employee_weekday_check',
        ),
        {
            'schema': 'time_recording',
            'extend_existing': True,
        },
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('employee.employees.id', ondelete='CASCADE'),
        nullable=False,
    )

    weekday: Mapped[str] = mapped_column(String(9), nullable=False)

    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    lunch_start: Mapped[datetime.time] = mapped_column(Time)
    lunch_end: Mapped[datetime.time] = mapped_column(Time)
    end_time: Mapped[datetime.time] = mapped_column(Time)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    updated_at: Mapped[datetime] = mapped_column(DateTime)
    updated_by: Mapped[int] = mapped_column(Integer)
    deleted_at: Mapped[datetime] = mapped_column(DateTime)
    deleted_by: Mapped[int] = mapped_column(Integer)

    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text('false'), nullable=False)
