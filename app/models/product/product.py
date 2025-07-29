# app/models/product.py

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger

log = setup_logger()


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(30), nullable=False)
    value_operation: Mapped[Numeric] = mapped_column(
        Numeric(2, 10), default=0.00
    )
    time_to_spend: Mapped[Interval] = mapped_column(Interval, nullable=False)
    commission: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"Product(id={self.id}, description={self.description})"

    @classmethod
    def list_products(cls): ...

    @classmethod
    def get_product(cls): ...

    @classmethod
    def create_product(cls): ...

    @classmethod
    def update_product(cls): ...

    @classmethod
    def delete_product(cls): ...


class ProductsEmployees(Base):
    __tablename__ = "products_employees"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("finance.products.id"), nullable=False
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey("public.employee.id"), nullable=False
    )
    is_check: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"""{self.id} created successfully"""

    @classmethod
    def list_products_employees(cls, employee_id: int): ...

    @classmethod
    def create_products_employees(cls, product_id: int, employee_id: int): ...

    @classmethod
    def delete_products_employees(cls): ...
