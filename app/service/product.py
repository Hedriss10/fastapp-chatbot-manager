# app/core/product.py
import os

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.log import setup_logger
from app.repositories.products_repositories import ProductRepositories
from app.schemas.pagination import PaginationParams
from app.schemas.product import (
    ProductInSchema,
    ProductOutSchema,
    ProductsInEmployeeSchema,
)

log = setup_logger()

UPLOAD_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static'
)

BASE_IMAGE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads'
)
URL_IMAGE_PREFIX = '/static/uploads'


class ProductsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProductRepositories(session)

    async def add_product(self, data: ProductInSchema) -> ProductOutSchema:
        await self.repository.add_product(data)
        return ProductOutSchema(message_id='product_created_successfully')

    async def list_products(self, pagination_params: PaginationParams):
        products, metadata = await self.repository.list_products(
            pagination_params
        )
        enriched_products = self.repository._add_images(products)
        return enriched_products, metadata

    async def get_product(self, id: int):
        return await self.repository.get_product(id)

    async def update_product(self, id: int, data: ProductOutSchema):
        await self.repository.update_product(id, data)
        return ProductOutSchema(message_id='product_updated_successfully')

    async def delete_product(self, id: int):
        await self.repository.delete_product(product_id=id)
        return ProductOutSchema(message_id='product_deleted_successfully')


class ProductEmployeeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ProductRepositories(session)

    async def add_products_employees(self, data: ProductsInEmployeeSchema):
        await self.repository.add_products_employee(data)
        return ProductOutSchema(
            message_id='product_employee_created_successfully'
        )

    async def list_employees_products(self, employee_id: int):
        return await self.repository.list_employees_products(
            employee_id=employee_id
        )
