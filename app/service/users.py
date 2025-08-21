from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils.pagination import PaginationParams
from app.repositories.users_repositories import UserRepositories
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepositories(session)

    async def add_users(self, data: UserCreate):
        return await self.user_repo.add_users(data)

    async def list_users(self, pagination_params: PaginationParams):
        return await self.user_repo.list_users(pagination_params)

    async def get_user(self, user_id: int):
        return await self.user_repo.get_user(user_id)

    async def update_users(self, user_id: int, users_update: UserUpdate):
        return await self.user_repo.update_users(user_id, users_update)

    async def delete_users(self, user_id: int):
        return await self.user_repo.delete_users(user_id)
