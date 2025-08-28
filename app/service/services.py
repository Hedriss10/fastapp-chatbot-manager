from app.repositories.service_schedule import ServiceScheduleRepository
from app.schemas.service import ScheduleInEmployee


class ServiceSchedule:
    def __init__(self, session):
        self.session = session
        self.service_schedule = ServiceScheduleRepository(session)

    async def add_block(self, block_data: ScheduleInEmployee):
        return await self.service_schedule.add_block_schedule(block_data)

    async def get_all_block(self):
        return await self.service_schedule.get_all_block()

    async def delete_block(self, block_id: int):
        return await self.service_schedule.delete_block_schedule(block_id)
