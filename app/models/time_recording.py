# app/models/time_recording.py
import uuid
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
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ScheduleEmployee(Base):
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

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
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

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')
    )

    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)

    is_deleted: Mapped[bool] = mapped_column(
        Boolean, server_default=text('false'), nullable=False
    )
