import uuid

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Interval,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModels


class Products(BaseModels):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'finance'}

    description: Mapped[str] = mapped_column(String(30), nullable=False)
    value_operation: Mapped[Numeric] = mapped_column(
        Numeric(10, 2), default=0.00, nullable=False
    )
    time_to_spend: Mapped[Interval] = mapped_column(
        Interval, nullable=False
    )
    commission: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False)


class ProductsEmployees(BaseModels):
    __tablename__ = 'products_employees'
    __table_args__ = {'schema': 'finance'}

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('finance.products.id'), nullable=False
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('employee.employees.id'), nullable=False
    )
    is_check: Mapped[bool] = mapped_column(Boolean, default=False)
