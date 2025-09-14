from datetime import datetime, timedelta
from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception.exceptions import DatabaseError
from app.core.log import setup_logger
from app.models.block import ScheduleBlock
from app.models.schedule import ScheduleService
from app.schemas.slots import SlotsInSchema

log = setup_logger()


class SlotsRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.schedule = ScheduleService
        self.block = ScheduleBlock

    async def list_slots(
        self,
        data: SlotsInSchema,
    ) -> List[Dict[str, datetime]]:
        """
        Gera slots disponíveis para um funcionário em um determinado dia.

        Args:
            employee_id (int): ID do funcionário.
            work_start (str): Hora inicial do expediente (HH:MM).
            work_end (str): Hora final do expediente (HH:MM).
            slot_minutes (int, optional): Duração do slot em minutos. \
                Default: 30.
            target_date (date, optional): Data para gerar os slots. \
                Default: hoje.

        Returns:
            List[Dict[str, datetime]]: \
            Lista de slots disponíveis com start/end.
        """
        try:
            target_date = data.target_date or datetime.now().date()

            # 1. Intervalo de trabalho
            start_dt = datetime.combine(
                target_date,
                datetime.strptime(data.work_start, '%H:%M').time(),
            )
            end_dt = datetime.combine(
                target_date,
                datetime.strptime(data.work_end, '%H:%M').time(),
            )

            # 2. Gera slots brutos
            slots = []
            current = start_dt
            while current < end_dt:
                slots.append({
                    'start': current,
                    'end': current + timedelta(minutes=data.slot_minutes),
                })
                current += timedelta(minutes=data.slot_minutes)

            # 3. Pega agendamentos existentes
            scheduled = await self.session.scalars(
                select(self.schedule.time_register).where(
                    self.schedule.employee_id == data.employee_id,
                    self.schedule.is_deleted == False,
                )
            )
            scheduled_times = set(scheduled.all())

            # 4. Pega bloqueios
            block_results = await self.session.execute(
                select(self.block.start_time, self.block.end_time).where(
                    self.block.employee_id == data.employee_id
                )
            )
            blocks = block_results.all()

            # 5. Filtra slots
            available = []
            for slot in slots:
                if slot['start'] in scheduled_times:
                    continue
                if any(b[0] <= slot['start'] < b[1] for b in blocks):
                    continue
                available.append(slot)

            return available

        except Exception as e:
            log.error(f'Error in list_slots: {e}', exc_info=True)
            DatabaseError('Error in list_slots')
