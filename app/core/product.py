# app/core/product.py


from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.product.product import Products
from app.schemas.pagination import PaginationParams

log = setup_logger()


class ProdudtCore:
    @staticmethod
    async def list_products(pagination: PaginationParams, db: Session):
        return await Products.list_products(
            pagination_params=pagination, db=db
        )

    async def get_product(id: int, db: Session):
        return await Products.get_product(id=id, db=db)

    async def add_product(data: Products, db: Session):
        return await Products.add_product(data, db)

    async def update_product(id: int, data: Products, db: Session):
        return await Products.update_product(id=id, data=data, db=db)

    async def delete_product(id: int, db: Session):
        return await Products.delete_product(id=id, db=db)
