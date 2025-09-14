from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.exceptions import DatabaseError
from app.core.log import setup_logger
from app.core.utils.metadata import Metadata
from app.models.employee import Employee
from app.models.product import Products
from app.models.schedule import ScheduleService
from app.models.users import User
from app.schemas.pagination import BuildMetadata, PaginationParams
from app.schemas.schedule import (
    ScheduleInSchema,
    ScheduleOutSchema,
    UpdateScheduleInSchema,
)

log = setup_logger()

SCHEDULE_FIELDS = [
    'product_id',
    'employee_id',
    'time_register',
]


class ScheduleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.schedule = ScheduleService
        self.employee = Employee
        self.user = User
        self.products = Products

    def make_naive(self, dt: datetime) -> datetime:
        if dt.tzinfo:
            return dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt

    async def add_schedule(self, schedule: ScheduleInSchema):
        try:
            stmt = (
                insert(self.schedule)
                .values(
                    time_register=self.make_naive(schedule.time_register),
                    product_id=schedule.product_id,
                    employee_id=schedule.employee_id,
                    user_id=schedule.user_id,
                    is_check=False,
                    is_awayalone=False,
                    is_deleted=False,
                    created_at=datetime.now(),
                )
                .returning(self.schedule.id)
            )

            result = await self.session.execute(stmt)
            await self.session.commit()
            schedule_id = result.scalar_one()

            return ScheduleOutSchema(
                message_id='schedule_created_successfully',
                schedule_id=schedule_id,
            )

        except Exception as e:
            await self.session.rollback()
            log.error(f'Error adding schedule: {e}')
            raise DatabaseError('Error adding schedule')

    async def list_schedule(
        self, pagination_params: PaginationParams
    ) -> Tuple[List[Dict[str, Any]], BuildMetadata]:
        try:
            stmt = (
                select(
                    self.schedule.id,
                    self.schedule.time_register,
                    self.employee.id.label('employee_id'),
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
                    self.products,
                    self.schedule.product_id == self.products.id,
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
                    stmt = stmt.filter(
                        self.user.username.ilike(filter_value)
                    )

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
                        f'Logger: Campo de ordenação inválido: \
                        {pagination_params.order_by}'
                    )

            # Total de registros
            total_count = await self.session.execute(
                select(func.count()).select_from(stmt.subquery())
            )
            total_count = total_count.scalar()

            # Paginação
            paginated_stmt = stmt.offset(
                (pagination_params.current_page - 1)
                * pagination_params.rows_per_page
            ).limit(pagination_params.rows_per_page)

            result = await self.session.execute(paginated_stmt)
            result = result.all()

            metadata = BuildMetadata(
                total_count=total_count,
                current_page=pagination_params.current_page,
                rows_per_page=pagination_params.rows_per_page,
                total_pages=(
                    total_count + pagination_params.rows_per_page - 1
                )
                // pagination_params.rows_per_page,
            )
            return Metadata(result).model_to_list(), metadata

        except Exception as e:
            self.session.rollback()
            log.error(f'Error listing schedules: {e}')
            raise DatabaseError('Error listing schedules')

    async def get_schedule(self, id: int) -> ScheduleService | None:
        try:
            stmt = (
                select(
                    self.schedule.id,
                    self.schedule.time_register,
                    self.employee.id.label('self.employee_id'),
                    Products.id.label('product_id'),
                    Products.description.label('product_name'),
                    func.to_char(
                        Products.time_to_spend, 'HH24:MI:SS'
                    ).label('time_to_spend'),
                    User.phone.label('phone'),
                    User.username.label('name_client'),
                    (
                        self.schedule.time_register
                        + Products.time_to_spend
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
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            self.session.rollback()
            log.error(f'Error getting schedule by id: {e}')
            raise DatabaseError('Error getting schedule by id')

    async def update_schedule(
        self, id: int, data: UpdateScheduleInSchema
    ) -> ScheduleOutSchema:
        try:
            stmt = (
                update(self.schedule)
                .where(self.schedule.id == id)
                .values(
                    **{
                        k: v
                        for k, v in data.dict(exclude_unset=True).items()
                        if k in SCHEDULE_FIELDS
                    },
                    updated_at=datetime.now(),
                )
            )
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                raise ValueError(f'Schedule with ID {id} not found.')

            await self.session.commit()
            return ScheduleOutSchema(
                message_id='schedule_updated_successfully'
            )

        except Exception as e:
            await self.session.rollback()
            log.error(f'Error updating schedule: {e}')
            raise DatabaseError('Error updating schedule')

    async def delete_schedule(self, id: int) -> ScheduleOutSchema | None:
        try:
            stmt = (
                update(self.schedule)
                .where(self.schedule.id == id)
                .values(is_deleted=True)
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return ScheduleOutSchema(
                message_id='schedule_deleted_successfully'
            )
        except Exception as e:
            self.session.rollback()
            log.error(f'Error deleting schedule: {e}')
            raise DatabaseError('Error deleting schedule')

    async def update_is_check(
        self, is_check: bool, user_id: int
    ) -> ScheduleService | None:
        try:
            stmt = (
                update(self.schedule)
                .where(self.schedule.user_id == user_id)
                .values(is_check=is_check, updated_at=datetime.now())
                .returning(self.schedule)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()
        except Exception as e:
            self.session.rollback()
            log.error(f'Error updating is_check: {e}')
            raise DatabaseError('Error updating is_check')
