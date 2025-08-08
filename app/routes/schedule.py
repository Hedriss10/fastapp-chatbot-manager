# app/routes/schedule.py

from fastapi import APIRouter, Depends
from app.core.schedule import ScheduleCore
from sqlalchemy.orm import Session
from app.schemas.schedule import ScheduleInSchema, ScheduleOutSchema
from app.schemas.pagination import PaginationParams
from app.db.depency import get_db
from fastapi.exceptions import HTTPException
from pydantic import ValidationError



schedule = APIRouter(prefix='/schedule', tags=['schedule'])


@schedule.post('', description='Add schedule', response_model=ScheduleOutSchema)
async def add_schedule(data: ScheduleInSchema, db: Session = Depends(get_db)):
    try:
        return ScheduleCore.add_schedule(data=data, db=db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while creating the schedule.',
        )

@schedule.get('/{id}', description='Get schedule of id', response_model=ScheduleOutSchema)
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

@schedule.get('', description='List all schedules', response_model=list[ScheduleOutSchema])
async def list_schedules(params: PaginationParams = Depends(), db: Session = Depends(get_db)):
    try:
        return ScheduleCore.list_schedules(db=db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while getting the schedules.',
        )
        
@schedule.put('/{id}', description='Update schedule of id', response_model=ScheduleOutSchema)
async def update_schedule(id: int, data: ScheduleInSchema, db: Session = Depends(get_db)):
    try:
        return ScheduleCore.update_schedule(id=id, data=data, db=db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while updating the schedule.',
        )
        

@schedule.delete('/{id}', description='Delete schedule of id')
async def delete_schedule(id: int, db: Session = Depends(get_db)):
    try:
        return ScheduleCore.delete_schedule(id=id, db=db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while deleting the schedule.',
        )