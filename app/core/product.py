# app/core/product.py


from app.models.product.product import Products
from app.schemas.pagination import PaginationParams
from sqlalchemy.orm import Session
from app.logs.log import setup_logger


log = setup_logger()


class ProdudtCore:
    @staticmethod
    async def list_products(pagination: PaginationParams, db: Session):
        return await Products.list_products(pagination_params=pagination, db=db)
    
    async def get_product(id: int, db: Session):
        return await Products.get_product(id=id, db=db)

    async def add_product(data: Products, db: Session):
        return await Products.add_product(data, db)

    async def update_product(data: Products, db: Session):
        return await Products.update_product(data, db)

    async def delete_product(id: int, db: Session):
        return await Products.delete_product(id=id, db=db)
