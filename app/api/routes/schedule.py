# app/routes/schedule.py
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.depency import get_db
from app.schemas.pagination import PaginationParams
from app.schemas.schedule import ScheduleInSchema, ScheduleOutSchema
from app.service.schedule import ScheduleService

schedule = APIRouter(prefix='/schedule', tags=['schedule'])


@schedule.post(
    '', description='Add schedule', response_model=ScheduleOutSchema
)
async def add_schedule(
    data: ScheduleInSchema, db: AsyncSession = Depends(get_db)
):
    try:
        return await ScheduleService(session=db).register_schedule(
            data=data
        )
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while creating the schedule.',
        )


@schedule.get(
    '/manageruser',
    description='Get schedule of id',
)
async def get_schedule(
    db: AsyncSession = Depends(get_db),
    id: int = Header(..., alias='Id'),
):
    try:
        result = await ScheduleService(session=db).get_schedule(id=id)
        return {'data': result}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while getting the schedule.',
        )


@schedule.get(
    '',
    description='List all schedules',
)
async def list_schedules(
    params: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        users, metadata = await ScheduleService(session=db).list_schedules(
            pagination_params=params
        )
        return {'data': users, 'metadata': metadata}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while getting the schedules.',
        )


@schedule.put(
    '/{id}',
    description='Update schedule of id',
    response_model=ScheduleOutSchema,
)
async def update_schedule(
    id: UUID, data: ScheduleInSchema, db: AsyncSession = Depends(get_db)
):
    try:
        return await ScheduleService(session=db).update_schedule(
            id=id, data=data
        )
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while updating the schedule.',
        )


@schedule.delete('/{id}', description='Delete schedule of id')
async def delete_schedule(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        return await ScheduleService(session=db).delete_schedule(id=id)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while deleting the schedule.',
        )
