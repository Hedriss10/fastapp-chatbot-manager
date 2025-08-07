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
    insert,
    select,
    text,
    update,
)
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger
from app.schemas.pagination import BuildMetadata, PaginationParams
from app.schemas.product import (
    ProductInSchema,
    ProductOutSchema,
)
from app.utils.metadata import Metadata

log = setup_logger()


PRODUCTS_FIELDS = [
    'description',
    'value_operation',
    'time_to_spend',
    'commission',
    'category',
]


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'finance'}

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
        return f'Product(id={self.id}, description={self.description})'

    @classmethod
    async def list_products(
        cls, pagination_params: PaginationParams, db: Session
    ) -> tuple[list[dict], BuildMetadata]:
        try:
            stmt = select(
                cls.id,
                cls.description,
                cls.value_operation,
                func.to_char(cls.time_to_spend, text("'HH24:MI:SS'")).label(
                    'time_to_spend'
                ),
                cls.commission,
                cls.category,
            ).where(cls.is_deleted == False)

            # Filtro
            if pagination_params.filter_by:
                filter_value = f'%{pagination_params.filter_by}%'
                try:
                    stmt = stmt.filter(
                        func.unaccent(cls.description).ilike(
                            func.unaccent(filter_value)
                        )
                    )
                except Exception:
                    stmt = stmt.filter(cls.description.ilike(filter_value))

            # Ordenação
            if pagination_params.order_by:
                try:
                    sort_column = getattr(cls, pagination_params.order_by)
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
                        f'Logger: Campo de ordenação inválido: {pagination_params.order_by}'
                    )

            total_count = db.execute(
                select(func.count()).select_from(stmt.subquery())
            ).scalar()

            paginated_stmt = stmt.offset(
                (pagination_params.current_page - 1)
                * pagination_params.rows_per_page
            ).limit(pagination_params.rows_per_page)

            result = db.execute(paginated_stmt).fetchall()

            metadata = BuildMetadata(
                total_count=total_count,
                current_page=pagination_params.current_page,
                rows_per_page=pagination_params.rows_per_page,
                total_pages=(total_count + pagination_params.rows_per_page - 1)
                // pagination_params.rows_per_page,
            )
            return Metadata(result).model_to_list(), metadata

        except Exception as e:
            log.exception(e)
            raise

    @classmethod
    async def get_product(cls, id: int, db: Session):
        try:
            stmt = select(
                cls.id,
                cls.description,
                cls.value_operation,
                func.to_char(cls.time_to_spend, text("'HH24:MI:SS'")).label(
                    'time_to_spend'
                ),
                cls.commission,
                cls.category,
            ).where(cls.id == id, cls.is_deleted == False)
            result = db.execute(stmt).fetchone()
            return Metadata(result).model_to_list()

        except Exception as e:
            log.error(f'Logger: Error get_product: {e}')
            raise

    @classmethod
    async def add_product(cls, data: ProductInSchema, db: Session):
        try:
            stmt = insert(cls).values(
                description=data.description,
                value_operation=data.value_operation,
                time_to_spend=data.time_to_spend,
                commission=data.commission,
                category=data.category,
            )
            db.execute(stmt)
            db.commit()
            return ProductOutSchema(message_id='product_created_successfully')
        except Exception as e:
            print('Coletando o erro ao add o produto', e)
            db.rollback()
            log.error('Error adding product')

    @classmethod
    async def update_product(cls, id: int, data: ProductInSchema, db: Session):
        try:
            prodcuts = db.query(cls).filter(cls.id == id).first()
            update_key = {}
            for key, value in data:
                if value is not None and key in PRODUCTS_FIELDS:
                    if hasattr(prodcuts, key):
                        setattr(prodcuts, key, value)
                        update_key[key] = value
            stmt = update(cls).where(cls.id == id).values(update_key)
            db.execute(stmt)
            db.commit()
            return ProductOutSchema(message_id='product_updated_successfully')
        except Exception as e:
            db.rollback()
            log.error(f'Logger: Error update_product: {e}')
            raise

    @classmethod
    async def delete_product(cls, id: int, db: Session):
        try:
            stmt = db.query(cls).filter(cls.id == id).first()
            stmt.is_deleted = True
            db.commit()
            return ProductOutSchema(message_id='product_deleted_successfully')
        except Exception as e:
            db.rollback()
            log.error(f'Logger: Error delete_product: {e}')
            raise


class ProductsEmployees(Base):
    __tablename__ = 'products_employees'
    __table_args__ = {'schema': 'finance'}

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('finance.products.id'), nullable=False
    )
    employee_id: Mapped[int] = mapped_column(
        ForeignKey('employee.employees.id'), nullable=False
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
