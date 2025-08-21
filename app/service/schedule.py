# app/core/schedule.py

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.log import setup_logger
from app.core.utils.metadata import Metadata
from app.models.employee import Employee
from app.models.product import Products
from app.models.schedule import ScheduleService
from app.models.users import User
from app.schemas.pagination import BuildMetadata, PaginationParams
from app.schemas.schedule import ScheduleInSchema, ScheduleOutSchema

log = setup_logger()


SCHEDULE_FIELDS = [
    'product_id',
    'employee_id',
    'time_register',
]


class ScheduleCore:
    def __init__(self, db: Session, *args, **kwargs):
        self.db = db
        self.schedule = ScheduleService
        self.employee = Employee
        self.user = User
        self.products = Products

    def add_schedule(self, data: ScheduleInSchema):
        try:
            return self.schedule.register_schedule(data=data, db=self.db)
        except Exception as e:
            log.error(f'Logger: Error add_schedule: {e}')
            raise

    async def list_schedules(self, pagination_params: PaginationParams):
        try:
            stmt = (
                select(
                    self.schedule.id,
                    self.schedule.time_register,
                    self.employee.id.label('self.employee_id'),
                    self.products.id.label('product_id'),
                    self.products.description.label('product_name'),
                    func.to_char(
                        self.products.time_to_spend, 'HH24:MI:SS'
                    ).label('time_to_spend'),
                    self.user.phone.label('phone'),
                    self.user.username.label('name_client'),
                    (
                        self.schedule.time_register
                        + self.products.time_to_spend
                    ).label('end_time'),
                    self.employee.username.label('name_employee'),
                )
                .join(
                    self.employee,
                    self.schedule.employee_id == self.employee.id,
                )
                .join(
                    self.products, self.schedule.product_id == self.products.id
                )
                .join(self.user, self.schedule.user_id == self.user.id)
                .where(
                    self.schedule.is_deleted == False,
                    self.schedule.is_check == False,
                )
            )

            # Filtro por nome
            if pagination_params.filter_by:
                filter_value = f'%{pagination_params.filter_by}%'
                try:
                    stmt = stmt.filter(
                        func.unaccent(self.user.username).ilike(
                            func.unaccent(filter_value)
                        )
                    )
                except Exception:
                    stmt = stmt.filter(self.user.username.ilike(filter_value))

            # Ordenação
            if pagination_params.order_by:
                try:
                    sort_column = getattr(
                        self.user, pagination_params.order_by
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
                        f'Logger: Campo de ordenação inválido: {pagination_params.order_by}'
                    )

            # Total de registros
            total_count = self.db.execute(
                select(func.count()).select_from(stmt.subquery())
            ).scalar()

            # Paginação
            paginated_stmt = stmt.offset(
                (pagination_params.current_page - 1)
                * pagination_params.rows_per_page
            ).limit(pagination_params.rows_per_page)

            result = self.db.execute(paginated_stmt).fetchall()

            metadata = BuildMetadata(
                total_count=total_count,
                current_page=pagination_params.current_page,
                rows_per_page=pagination_params.rows_per_page,
                total_pages=(total_count + pagination_params.rows_per_page - 1)
                // pagination_params.rows_per_page,
            )

            return Metadata(result).model_to_list(), metadata
        except Exception as e:
            log.error(f'Logger: Error list_schedules: {e}')
            raise

    async def get_schedule(self, id: int):
        try:
            stmt = (
                select(
                    self.schedule.id,
                    self.schedule.time_register,
                    self.employee.id.label('self.employee_id'),
                    Products.id.label('product_id'),
                    Products.description.label('product_name'),
                    func.to_char(Products.time_to_spend, 'HH24:MI:SS').label(
                        'time_to_spend'
                    ),
                    User.phone.label('phone'),
                    User.username.label('name_client'),
                    (
                        self.schedule.time_register + Products.time_to_spend
                    ).label('end_time'),
                    self.employee.username.label('name_self.employee'),
                )
                .join(
                    self.employee,
                    self.schedule.employee_id == self.employee.id,
                )
                .join(Products, self.schedule.product_id == Products.id)
                .join(User, self.schedule.user_id == User.id)
                .where(
                    self.schedule.is_deleted == False,
                    self.schedule.user_id == id,
                    self.schedule.is_check == False,
                )
            )
            result_raw = self.db.execute(stmt).fetchall()
            return Metadata(result_raw).model_to_list()
        except Exception as e:
            log.error(f'Logger: Error get_schedule: {e}')
            raise

    async def update_schedule(self, id: int, data: ScheduleInSchema):
        try:
            schedule = self.db.query(self.schedule).filter_by(id=id).first()
            if not schedule:
                log.error(f'Schedule with ID {id} not found.')
                raise ValueError(f'Schedule with ID {id} not found.')

            for key, value in data:
                if value is not None and key in SCHEDULE_FIELDS:
                    setattr(schedule, key, value)

            schedule.updated_at = datetime.now()
            self.db.add(schedule)
            self.db.commit()
            return ScheduleOutSchema(
                message_id='schedule_updated_successfully'
            )

        except Exception as e:
            self.db.rollback()
            log.error(f'Logger: Error update_schedule: {e}')
            raise

    async def delete_schedule(self, id: int):
        try:
            stmt = (
                self.db.query(self.schedule)
                .filter(self.schedule.id == id)
                .first()
            )
            stmt.is_deleted = True
            self.db.commit()
            return ScheduleOutSchema(
                message_id='schedule_deleted_successfully'
            )
        except Exception as e:
            self.db.rollback()
            log.error(f'Logger: Error delete_schedule: {e}')
            raise
