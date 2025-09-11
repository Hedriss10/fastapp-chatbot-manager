from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.slots_repositories import SlotsRepositories
from app.schemas.slots import SlotSchema, SlotsInSchema


class SlotService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.slot_repo = SlotsRepositories(session)

    async def list_slots(self, data: SlotsInSchema) -> List[SlotSchema]:
        slots = await self.slot_repo.list_slots(data)
        return [SlotSchema(**s) for s in slots]
