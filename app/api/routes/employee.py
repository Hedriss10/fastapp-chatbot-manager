# app/routes/employee.py
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.service.employee import EmployeeService

employee = APIRouter(prefix='/employee', tags=['employee'])


@employee.post(
    '', response_model=EmployeeOut, status_code=status.HTTP_201_CREATED
)
async def add_employee(
    data: EmployeeBase, db: AsyncSession = Depends(get_db)
):
    try:
        return await EmployeeService(session=db).add_employee(data)
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
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        employees, metadata = await EmployeeService(
            session=db
        ).list_employee(pagination)
        return {'data': employees, 'metadata': metadata}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while listing employees.',
        )


@employee.get(
    '/{id}',
    response_model=EmployeeGetIdOut,
    status_code=status.HTTP_200_OK,
)
async def get_employee(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        employee = await EmployeeService(session=db).get_employee(id)
        if not employee:
            raise HTTPException(
                status_code=404, detail='Employee not found.'
            )
        return employee
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while retrieving the employee.',
        )


@employee.put(
    '/{id}',
    response_model=EmployeeUpdateOut,
    status_code=status.HTTP_200_OK,
)
async def update_employee(
    id: UUID, data: EmployeeUpdate, db: AsyncSession = Depends(get_db)
):
    try:
        updated_employee = await EmployeeService(
            session=db
        ).update_employee(employee_id=id, data=data)
        if not updated_employee:
            raise HTTPException(
                status_code=404, detail='Employee not found.'
            )
        return updated_employee
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while updating the employee.',
        )


@employee.delete(
    '/{id}',
    response_model=EmployeeDeleteOut,
    status_code=status.HTTP_200_OK,
)
async def delete_employee(id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        deleted_employee = await EmployeeService(
            session=db
        ).delete_employee(id)
        if not deleted_employee:
            raise HTTPException(
                status_code=404, detail='Employee not found.'
            )
        return EmployeeDeleteOut(
            message_id='employee_deleted_successfully'
        )
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while deleting the employee.',
        )
