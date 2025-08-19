# app/routes/employee.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.employee import EmployeeCore
from app.db.depency import get_db
from app.schemas.employee import (
    EmployeeBase,
    EmployeeDeleteOut,
    EmployeeGetIdOut,
    EmployeeOut,
    EmployeeUpdate,
    EmployeeUpdateOut,
)
from app.schemas.pagination import PaginationParams

employee = APIRouter(prefix='/employee', tags=['employee'])


@employee.post(
    '', response_model=EmployeeOut, status_code=status.HTTP_201_CREATED
)
async def add_employee(data: EmployeeBase, db: Session = Depends(get_db)):
    try:
        return EmployeeCore(db=db).add_employee(data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while creating the employee.',
        )


@employee.get(
    '', description='List all employees', status_code=status.HTTP_200_OK
)
async def list_employees(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    try:
        employees, metadata = EmployeeCore(db=db).list_employees(pagination)
        return {'data': employees, 'metadata': metadata}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while listing employees.',
        )


@employee.get(
    '/{id}', response_model=EmployeeGetIdOut, status_code=status.HTTP_200_OK
)
async def get_employee(id: int, db: Session = Depends(get_db)):
    try:
        employee = EmployeeCore(db=db).get_employee(id)
        if not employee:
            raise HTTPException(status_code=404, detail='Employee not found.')
        return employee
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while retrieving the employee.',
        )


@employee.put(
    '/{id}', response_model=EmployeeUpdateOut, status_code=status.HTTP_200_OK
)
async def update_employee(
    id: int, data: EmployeeUpdate, db: Session = Depends(get_db)
):
    try:
        updated_employee = EmployeeCore(db=db).update_employee(id, data)
        if not updated_employee:
            raise HTTPException(status_code=404, detail='Employee not found.')
        return updated_employee
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while updating the employee.',
        )


@employee.delete(
    '/{id}', response_model=EmployeeDeleteOut, status_code=status.HTTP_200_OK
)
async def delete_employee(id: int, db: Session = Depends(get_db)):
    try:
        deleted_employee = EmployeeCore(db=db).delete_employee(id)
        if not deleted_employee:
            raise HTTPException(status_code=404, detail='Employee not found.')
        return EmployeeDeleteOut(message_id='employee_deleted_successfully')
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while deleting the employee.',
        )
