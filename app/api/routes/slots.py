from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.depency import get_db
from app.schemas.slots import SlotSchema, SlotsInSchema
from app.service.slots import SlotService

slots = APIRouter(prefix='/slot', tags=['slot'])


@slots.post('', description='List available slots for an employee', response_model=List[SlotSchema])
async def list_slots(data: SlotsInSchema, db: AsyncSession = Depends(get_db)):
    try:
        return await SlotService(session=db).list_slots(data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while listing the slots.',
        )
