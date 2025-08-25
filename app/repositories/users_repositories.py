from typing import Any, Dict, List, Tuple

from sqlalchemy import func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.exceptions import DatabaseError
from app.core.log import setup_logger
from app.core.utils.metadata import Metadata
from app.models.users import User
from app.schemas.pagination import BuildMetadata, PaginationParams
from app.schemas.users import (
    UserCreate,
    UserDeleteOut,
    UserUpdate,
    UserUpdateOut,
)

log = setup_logger()


USER_FIELDS = [
    'username',
    'lastname',
    'phone',
]


class UserRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = User

    async def add_users(self, data: UserCreate) -> int:
        try:
            stmt = (
                insert(self.user)
                .values(
                    username=data.username,
                    lastname=data.lastname,
                    phone=data.phone,
                )
                .returning(
                    self.user.id,
                    self.user.username,
                    self.user.lastname,
                    self.user.phone,
                )
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            row = result.fetchone()
            return dict(row._mapping) if row else {}
        except Exception as e:
            await self.session.rollback()
            log.error(f'Error adding user: {e}')
            raise DatabaseError('Error adding user to the database')

    async def get_user(self, user_id: int):
        try:
            user = select(self.user).where(self.user.id == user_id)
            result = await self.session.execute(user)
            return result.scalar()
        except Exception as e:
            log.error(f'Error getting user {user_id}: {e}')
            raise DatabaseError('Error getting user from the database')

    async def list_users(
        self, pagination_params: PaginationParams
    ) -> Tuple[List[Dict[str, Any]], BuildMetadata]:
        try:
            stmt = select(
                self.user.id,
                self.user.username,
                self.user.lastname,
                self.user.phone,
            ).where(self.user.is_deleted.__eq__(False))

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
                total_pages=(total_count + pagination_params.rows_per_page - 1)
                // pagination_params.rows_per_page,
            )
            return Metadata(result).model_to_list(), metadata

        except Exception as e:
            log.error(f'Error listing users: {e}')
            raise DatabaseError('Error listing users from the database')

    async def update_users(
        self, user_id: int, data: UserUpdate
    ) -> UserUpdateOut:
        try:
            user = await self.session.get(self.user, user_id)
            if not user:
                return UserUpdateOut(message_id='user_not_found')

            update_key = {}
            for key, value in data.dict(exclude_unset=True).items():
                if value is not None and key in USER_FIELDS:
                    update_key[key] = value

            if update_key:
                stmt = (
                    update(self.user)
                    .where(self.user.id == user_id)
                    .values(update_key)
                )
                await self.session.execute(stmt)
                await self.session.commit()

            return UserUpdateOut(message_id='user_updated_successfully')

        except Exception as e:
            log.error(f'Error updating user {user_id}: {e}')
            raise DatabaseError('Error updating user in the database')

    async def delete_users(self, user_id: int) -> UserDeleteOut:
        try:
            stmt = (
                update(self.user)
                .where(self.user.id == user_id)
                .values(is_deleted=True)
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return UserDeleteOut(message_id='user_deleted_successfully')

        except Exception as e:
            log.error(f'Error deleting user {user_id}: {e}')
            raise DatabaseError('Error deleting user from the database')
