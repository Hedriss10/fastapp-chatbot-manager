from datetime import timedelta
from typing import Optional
from uuid import UUID

from fastapi import File, Form
from pydantic import BaseModel, Field


class ProductArgumentSchemas:
    arguments_description = (Form(...),)
    arguments_value_operation = (Form(...),)
    arguments_time_to_spend = (Form(...),)
    arguments_commission = (Form(...),)
    arguments_category = (Form(None),)
    arguments_image = (File(None),)


class ProductInSchema(BaseModel):
    description: str = Field(..., max_length=30)
    value_operation: float = Field(default=0.00)
    time_to_spend: timedelta
    commission: float = Field(default=0.0, ge=0.0)
    category: Optional[str] = Field(default=None, max_length=20)
    image: Optional[str] = None


class ProductOutSchema(BaseModel):
    message_id: str


class ProductUpdateSchema(BaseModel):
    description: str
    value_operation: float
    time_to_spend: str
    commission: float
    category: str


class ProductDeleteSchema(BaseModel):
    id: UUID


class ProductsInEmployeeSchema(BaseModel):
    product_id: UUID
    employee_id: UUID
    is_check: Optional[bool] = False
