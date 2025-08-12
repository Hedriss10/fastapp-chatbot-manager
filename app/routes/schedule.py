# app/routes/schedule.py

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.schedule import ScheduleCore
from app.db.depency import get_db
from app.schemas.pagination import PaginationParams
from app.schemas.schedule import ScheduleInSchema, ScheduleOutSchema

schedule = APIRouter(prefix='/schedule', tags=['schedule'])


@schedule.post(
    '', description='Add schedule', response_model=ScheduleOutSchema
)
async def add_schedule(data: ScheduleInSchema, db: Session = Depends(get_db)):
    try:
        return ScheduleCore().add_schedule(data=data, db=db)
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
async def get_schedule(id: int, db: Session = Depends(get_db)):
    try:
        return ScheduleCore.get_schedule(id=id, db=db)
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
    params: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    try:
        users, metadata = await ScheduleCore().list_schedules(
            pagination_params=params, db=db
        )
        return {'data': users, 'metadata': metadata}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        print('Erroor', e)
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
    id: int, data: ScheduleInSchema, db: Session = Depends(get_db)
):
    try:
        return await ScheduleCore().update_schedule(id=id, data=data, db=db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while updating the schedule.',
        )


@schedule.delete('/{id}', description='Delete schedule of id')
async def delete_schedule(id: int, db: Session = Depends(get_db)):
    try:
        return await ScheduleCore().delete_schedule(id=id, db=db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        print('Coletnado o erro', e)
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while deleting the schedule.',
        )
