# app/models/messages.py

from datetime import datetime

from db.db import Base
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Integer,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column


class SummaryMessage(Base):
    __tablename__ = "summary_message"
    __table_args__ = {"schema": "campaign"}

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"SummaryMessage(id={self.id}, message={self.message})"
