from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.time_recording import ScheduleEmployee
from app.models.block import ScheduleBlock
from app.schemas.schedule import ScheduleInBlock
from app.schemas.service import ScheduleEmployeeOut
from app.core.exception.exceptions import DatabaseError
from app.core.utils.metadata import Metadata
from app.core.log import setup_logger

log = setup_logger()


class ServiceScheduleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.schedule_employee = ScheduleEmployee
        self.schedule_block = ScheduleBlock

    async def add_block_schedule(self, block_data: ScheduleInBlock):
        try:
            new_block = insert(self.schedule_block).values(
                **block_data.model_dump()
            )
            await self.session.execute(new_block)
            await self.session.commit()
            return ScheduleEmployeeOut(message_id='added_block')
        except Exception:
            await self.session.rollback()
            raise DatabaseError('Failed to add block schedule')

    async def get_all_block(self):
        try:
            stmt = select(
                self.schedule_block.id,
                self.schedule_block.start_time,
                self.schedule_block.end_time,
                self.schedule_block.employee_id,
            ).where(self.schedule_block.is_deleted.__eq__(False))

            result = await self.session.execute(stmt)
            result = result.all()
            return Metadata(result).model_to_list()
        except Exception as e:
            log.error(f'Error fetching blocks: {e}')
            raise DatabaseError('Failed to fetch block schedules')

    async def delete_block_schedule(self, block_id: int):
        try:
            stmt = (
                update(self.schedule_block)
                .where(self.schedule_block.id == block_id)
                .values(is_deleted=True)
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return ScheduleEmployeeOut(message_id='delete_block_success')

        except Exception as e:
            await self.session.rollback()
            log.error(f'Error deleting block {block_id}: {e}')
            raise DatabaseError('Error deleting block from the database')
