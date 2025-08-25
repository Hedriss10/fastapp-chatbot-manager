from datetime import datetime
import os
from typing import Any, Dict, List, Tuple

from sqlalchemy import func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.exceptions import DatabaseError
from app.core.log import setup_logger
from app.models.product import Products, ProductsEmployees
from app.schemas.pagination import BuildMetadata, PaginationParams
from app.schemas.product import (
    ProductInSchema,
    ProductOutSchema,
    ProductUpdateSchema,
    ProductsInEmployeeSchema,
)
from app.settings.settings import settings

log = setup_logger()


UPLOAD_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static'
)

BASE_IMAGE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads'
)

URL_IMAGE_PREFIX = '/static/uploads'

PRODUCTS_FIELDS = [
    'description',
    'value_operation',
    'time_to_spend',
    'commission',
    'category',
]


class HelpersProducts:
    def _add_images(self, products: List[dict]) -> List[dict]:
        """Enriquece os produtos com URL de imagem"""
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

        return enriched_products


class ProductRepositories(HelpersProducts):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product = Products
        self.products_employee = ProductsEmployees

    async def add_product(self, data: ProductInSchema) -> dict:
        try:
            # Gera dict e remove 'image', que não vai para o banco
            product_dict = data.model_dump()
            product_dict.pop('image', None)

            product = Products(**product_dict)
            self.session.add(product)
            await self.session.commit()
            await self.session.refresh(product)

            product_out = dict(product.__dict__)
            product_out.pop('_sa_instance_state', None)

            enriched = self._add_images([product_out])[0]
            return enriched
        except Exception as e:
            log.error(f'Logger: Error add_product: {e}')
            await self.session.rollback()
            raise DatabaseError('Erro ao criar produto')

    async def list_products(
        self, pagination_params: PaginationParams
    ) -> Tuple[List[Dict[str, Any]], BuildMetadata]:
        try:
            stmt = select(
                self.product.id,
                self.product.description,
                self.product.value_operation,
                func.to_char(self.product.time_to_spend, 'HH24:MI:SS').label(
                    'time_to_spend'
                ),
                self.product.commission,
                self.product.category,
            ).where(self.product.is_deleted.is_(False))

            if pagination_params.filter_by:
                filter_value = f'%{pagination_params.filter_by}%'
                stmt = stmt.filter(
                    func.unaccent(self.product.description).ilike(filter_value)
                )

            if pagination_params.order_by:
                try:
                    sort_column = getattr(
                        self.product, pagination_params.order_by
                    )
                    sort_direction = (
                        pagination_params.sort_by or 'asc'
                    ).lower()
                    stmt = stmt.order_by(
                        sort_column.asc()
                        if sort_direction == 'asc'
                        else sort_column.desc()
                    )
                except AttributeError:
                    log.warning(
                        f'Campo de ordenação inválido: {pagination_params.order_by}'
                    )

            total_count = await self.session.scalar(
                select(func.count()).select_from(stmt.subquery())
            )

            paginated_stmt = stmt.offset(
                (pagination_params.current_page - 1)
                * pagination_params.rows_per_page
            ).limit(pagination_params.rows_per_page)

            result = await self.session.execute(paginated_stmt)
            result = result.mappings().all()  # pega como dict-like

            metadata = BuildMetadata(
                total_count=total_count,
                current_page=pagination_params.current_page,
                rows_per_page=pagination_params.rows_per_page,
                total_pages=(total_count + pagination_params.rows_per_page - 1)
                // pagination_params.rows_per_page,
            )

            enriched = self._add_images(result)

            return enriched, metadata

        except SQLAlchemyError as db_err:
            log.error(f'Database error while listing products: {db_err}')
            raise DatabaseError()

        except Exception as e:
            log.exception(f'Unexpected error in list_products: {e}')
            raise DatabaseError('Erro inesperado ao listar produtos')

    async def get_product(self, id: int) -> Dict[str, Any]:
        try:
            stmt = select(
                self.product.id,
                self.product.description,
                self.product.value_operation,
                func.to_char(self.product.time_to_spend, 'HH24:MI:SS').label(
                    'time_to_spend'
                ),
                self.product.commission,
                self.product.category,
            ).where(self.product.id == id, self.product.is_deleted.is_(False))

            result = await self.session.execute(stmt)
            product = result.mappings().first()

            if not product:
                log.warning(f'Product not found: {id}')
                return {'error': 'Product not found'}

            # Enriquecimento
            enriched_product = self._add_images([product])
            return enriched_product[0]

        except Exception as e:
            log.error(f'Logger: Error get_product: {e}')
            raise

    async def update_product(self, id: int, data: ProductUpdateSchema):
        try:
            prodcuts = select(self.product).where(self.product.id == id)
            updated_key = {}
            for key, value in data:
                if hasattr(prodcuts, key):
                    setattr(prodcuts, key, value)
                    updated_key[key] = value
            stmt = (
                update(self.product)
                .where(self.product.id == id)
                .values(updated_key)
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            self.session.rollback()
            log.error(f'Logger: Error update_product: {e}')
            raise DatabaseError('Erro inesperado ao atualizar produto')

    async def delete_product(self, product_id: int):
        try:
            stmt = (
                update(self.product)
                .where(self.product.id == product_id)
                .values(is_deleted=True)
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            self.session.rollback()
            log.error(f'Logger: Error delete_product: {e}')
            raise DatabaseError('Erro inesperado ao deletar produto')

    async def add_products_employee(self, data: ProductsInEmployeeSchema):
        try:
            stmt = insert(self.products_employee).values(
                product_id=data.product_id,
                created_at=datetime.now(),
                employee_id=data.employee_id
            )
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            self.session.rollback()
            log.error(f'Logger: Error add_products_employee: {e}')
            raise DatabaseError('Erro inesperado ao adicionar produtos ao funcionário')

    async def list_employees_products(self, employee_id: int):
        try:
            stmt = (
                select(
                    self.product.id,
                    self.product.description,
                    self.product.value_operation,
                    func.to_char(self.product.time_to_spend, 'HH24:MI:SS').label(
                        'time_to_spend'
                    ),
                    self.product.commission,
                    self.product.category,
                )
                .join(
                    self.products_employee,
                    self.product.id == self.products_employee.product_id,
                )
                .where(
                    self.products_employee.employee_id == employee_id,
                    self.product.is_deleted.__eq__(False),
                )
            )
            result = await self.session.execute(stmt)
            result = result.mappings().all()  # pega como dict-like
            
            enriched = self._add_images(result)
            return enriched
        except Exception as e:
            self.session.rollback()
            log.error(f'Logger: Error add_products_employee: {e}')
            raise DatabaseError('Erro inesperado ao adicionar produtos ao funcionário')
    
    
