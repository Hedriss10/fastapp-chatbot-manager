from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.depency import get_db
from app.schemas.service import ScheduleInEmployee
from app.service.services import ServiceSchedule

service = APIRouter(prefix='/service', tags=['service'])


@service.post('/block', description='Create block schedule')
async def add_block(
    block_data: ScheduleInEmployee, db: AsyncSession = Depends(get_db)
):
    try:
        return await ServiceSchedule(session=db).add_block(block_data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception:
        raise HTTPException(
            status_code=500, detail='Internal Server Error'
        )


@service.get('/block', description='Get all block schedules')
async def get_all_block(db: AsyncSession = Depends(get_db)):
    try:
        return await ServiceSchedule(session=db).get_all_block()
    except Exception:
        raise HTTPException(
            status_code=500, detail='Internal Server Error'
        )


@service.delete('/block/{block_id}', description='Delete block schedule')
async def delete_block(block_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await ServiceSchedule(session=db).delete_block(block_id)
    except Exception:
        raise HTTPException(
            status_code=500, detail='Internal Server Error'
        )
