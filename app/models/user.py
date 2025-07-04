# app/models/user.py

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.db import Base as db


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(db.String(120), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(40), nullable=False)
    session_token: Mapped[str] = mapped_column(db.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(db.Boolean, default=False)

    def __repr__(self):
        return f"""{self.username} created successfully"""
