from datetime import timedelta
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ProductInSchema(BaseModel):
    description: str = Field(..., max_length=30)
    value_operation: Decimal = Field(default=0.00, ge=0)
    time_to_spend: timedelta
    commission: float = Field(default=0.0, ge=0.0)
    category: Optional[str] = Field(default=None, max_length=20)


class ProductOutSchema(BaseModel):
    message_id: str


class ProductUpdateSchema(BaseModel):
    description: str
    value_operation: float
    time_to_spend: str
    commission: float
    category: str


class ProductDeleteSchema(BaseModel):
    id: int


class ProductEmployeeInSchema(BaseModel):
    employee_id: int
    product_id: int
