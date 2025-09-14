from datetime import datetime
from typing import Any, Dict, List, Tuple

from passlib.context import CryptContext
from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.exceptions import DatabaseError
from app.core.log import setup_logger
from app.core.utils.metadata import Metadata
from app.models.employee import Employee
from app.schemas.employee import (
    EmployeeBase,
    EmployeeGetIdOut,
    EmployeeOut,
    EmployeeUpdate,
    EmployeeUpdateOut,
)
from app.schemas.pagination import BuildMetadata, PaginationParams

EMPLOYEE_FIELDS = [
    'username',
    'date_of_birth',
    'phone',
    'role',
]

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

log = setup_logger()


class EmployeeRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.employee = Employee

    async def add_employee(self, data: EmployeeBase) -> EmployeeOut:
        try:
            stmt = insert(self.employee).values(
                username=data.username,
                date_of_birth=data.date_of_birth,
                phone=data.phone,
                role=data.role,
                password=pwd_context.hash(data.password),
            )
            await self.session.execute(stmt)
            await self.session.commit()

            return EmployeeOut(message_id='employee_created_successfully')
        except Exception as e:
            await self.session.rollback()
            log.error(f'Error adding employee: {e}')
            raise DatabaseError('Error adding employee to the database')

    async def list_employee(
        self, pagination_params: PaginationParams
    ) -> Tuple[List[Dict[str, Any]], BuildMetadata]:
        try:
            stmt = select(
                self.employee.id,
                self.employee.username,
                self.employee.date_of_birth,
                self.employee.phone,
                self.employee.role,
            ).where(self.employee.is_deleted.__eq__(False))

            # Filtro por nome
            if pagination_params.filter_by:
                filter_value = f'%{pagination_params.filter_by}%'
                try:
                    stmt = stmt.filter(
                        func.unaccent(self.employee.username).ilike(
                            func.unaccent(filter_value)
                        )
                    )
                except Exception:
                    stmt = stmt.filter(
                        self.employee.username.ilike(filter_value)
                    )

            # Ordenação
            if pagination_params.order_by:
                try:
                    sort_column = getattr(
                        self.employee, pagination_params.order_by
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
            log.error(f'Error listing employees: {e}')
            raise DatabaseError(
                'Error listing employees from the database'
            )

    async def get_employee_by_id(
        self, employee_id: int
    ) -> Employee | None:
        try:
            stmt = select(self.employee).where(
                self.employee.id == employee_id,
                self.employee.is_deleted.__eq__(False),
            )
            result = await self.session.execute(stmt)
            result = result.scalar_one_or_none()

            return EmployeeGetIdOut(**result.__dict__) if result else None

        except Exception as e:
            log.error(f'Error getting employee {employee_id}: {e}')
            raise DatabaseError('Error getting employee from the database')

    async def update_employee(
        self, employee_id: int, data: EmployeeUpdate
    ):
        try:
            stmt = await self.session.get(self.employee, employee_id)
            if not stmt:
                return EmployeeUpdateOut(message_id='employee_not_found')

            update_key = {}
            for key, value in data.dict(exclude_unset=True).items():
                if value is not None and key in EMPLOYEE_FIELDS:
                    if key == 'date_of_birth':
                        if isinstance(value, str):
                            try:
                                value = datetime.fromisoformat(
                                    value
                                ).date()
                            except ValueError:
                                value = datetime.strptime(
                                    value, '%Y-%m-%d'
                                ).date()
                    update_key[key] = value

            if update_key:
                stmt = (
                    update(self.employee)
                    .where(self.employee.id == employee_id)
                    .values(update_key)
                )
                await self.session.execute(stmt)
                await self.session.commit()

            return EmployeeUpdateOut(
                message_id='employee_updated_successfully'
            )

        except Exception as e:
            self.session.rollback()
            log.error(f'Error updating employee {employee_id}: {e}')
            raise DatabaseError('Error updating employee in the database')

    async def delete_employee(self, employee_id: int):
        try:
            stmt = (
                update(self.employee)
                .where(self.employee.id == employee_id)
                .values(is_deleted=True)
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return EmployeeOut(message_id='employee_deleted_successfully')
        except Exception as e:
            self.session.rollback()
            log.error(f'Error deleting employee {employee_id}: {e}')
            raise DatabaseError(
                'Error deleting employee from the database'
            )
