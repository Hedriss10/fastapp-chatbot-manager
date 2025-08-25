# app/core/schedule.py


from sqlalchemy.ext.asyncio import AsyncSession

from app.core.log import setup_logger
from app.models.schedule import ScheduleService
from app.repositories.schedule_repositories import ScheduleRepository
from app.schemas.pagination import PaginationParams
from app.schemas.schedule import ScheduleInSchema, ScheduleOutSchema

log = setup_logger()


class ScheduleService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = ScheduleRepository(session)

    async def register_schedule(
        self, data: ScheduleInSchema
    ) -> ScheduleOutSchema:
        return await self.repo.add_schedule(data)

    async def list_schedules(self, pagination_params: PaginationParams):
        return await self.repo.list_schedule(pagination_params)

    async def get_schedule(self, id: int) -> ScheduleService | None:
        return await self.repo.get_schedule(id)

    async def update_schedule(
        self, id: int, data: ScheduleInSchema
    ) -> ScheduleOutSchema:
        return await self.repo.update_schedule(id, data)

    async def delete_schedule(self, id: int) -> ScheduleOutSchema:
        return await self.repo.delete_schedule(id)
