import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BaseModels(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[PG_UUID] = mapped_column(PG_UUID, nullable=True)
    deleted_by: Mapped[PG_UUID] = mapped_column(PG_UUID, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
