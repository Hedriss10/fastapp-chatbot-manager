# app/models/product.py

from datetime import datetime
from sqlalchemy import Numeric, Interval
from sqlalchemy.orm import Mapped, mapped_column
from app.db.db import db

class Products(db.Model):
    __tablename__ = "products"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(db.String(30), nullable=False)
    value_operation: Mapped[Numeric] = mapped_column(
        db.Numeric(2, 10), default=0.00
    )
    time_to_spend: Mapped[Interval] = mapped_column(Interval, nullable=False)
    commission: Mapped[float] = mapped_column(db.Float, nullable=False)
    category: Mapped[str] = mapped_column(db.String(20), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(db.Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(db.Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(db.Boolean, default=False)

    def __repr__(self):
        return f"""{self.description} created successfully"""