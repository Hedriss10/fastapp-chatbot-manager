# app/core/product.py
import os

from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.product.product import Products
from app.schemas.pagination import PaginationParams
from app.settings.settings import settings

log = setup_logger()

UPLOAD_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static'
)

BASE_IMAGE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads'
)
URL_IMAGE_PREFIX = '/static/uploads'


class ProdudtCore:
    @staticmethod
    async def list_products(pagination: PaginationParams, db: Session):
        products, metadata = await Products.list_products(pagination, db)

        enriched_products = []
        for product in products:
            product_dict = dict(product)
            # Ex: Combo fade → product_images_Combo fade
            folder_name = f'product_images_{product_dict["description"]}'
            image_url = None

            # Caminha por todos os diretórios dentro de BASE_IMAGE_DIR
            for root, dirs, files in os.walk(BASE_IMAGE_DIR):
                if folder_name in dirs:
                    full_folder_path = os.path.join(root, folder_name)
                    image_files = [
                        f
                        for f in os.listdir(full_folder_path)
                        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
                    ]
                    if image_files:
                        # Gera o caminho relativo para servir como URL
                        relative_path = os.path.relpath(
                            os.path.join(full_folder_path, image_files[0]),
                            os.path.join(BASE_IMAGE_DIR),
                        )
                        image_url = f'{settings.backend_base_url}{URL_IMAGE_PREFIX}/{relative_path.replace(os.sep, "/")}'
                    break  # Encontrou a pasta, não precisa continuar

            if not image_url:
                image_url = f'{URL_IMAGE_PREFIX}/default.jpg'

            product_dict['image_url'] = image_url
            enriched_products.append(product_dict)

        return enriched_products, metadata

    async def get_product(id: int, db: Session):
        return await Products.get_product(id=id, db=db)

    async def add_product(data: Products, db: Session):
        return await Products.add_product(data, db)

    async def update_product(id: int, data: Products, db: Session):
        return await Products.update_product(id=id, data=data, db=db)

    async def delete_product(id: int, db: Session):
        return await Products.delete_product(id=id, db=db)
