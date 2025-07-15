# app/models/user.py

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger

log = setup_logger()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    session_token: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"""{self.username} created successfully"""

    @classmethod
    def get_by_id_user(cls, send_number: int, db: Session) -> Optional[int]:
        try:
            user_id = db.query(cls.id).filter(cls.phone == send_number).first()
            return user_id.id if user_id else None
        except Exception as e:
            log.error(f"Logger: error in colect ID user{e}")
            return None
        
    @classmethod
    def add_users(cls): ...
