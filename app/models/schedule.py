import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.log import setup_logger
from app.db.base import Base

log = setup_logger()


class ScheduleService(Base):
    __tablename__ = 'schedule'
    __table_args__ = {'schema': 'service'}

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    time_register: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
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
