# app/routes/employee.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from app.schemas.employee import (
    EmployeeBase,
    EmployeeOut,
    EmployeeUpdate,
    EmployeeUpdateOut,
    EmployeeDeleteOut,
)
from app.schemas.pagination import PaginationParams

from app.db.depency import get_db
from sqlalchemy.orm import Session

from app.core.employee import EmployeeCore

employee = APIRouter(prefix="/employee", tags=["employee"])


@employee.post("", response_model=EmployeeOut)
async def add_employee(data: EmployeeBase, db: Session = Depends(get_db)):
    try:
        return EmployeeCore.add_employee(data, db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating the employee.",
        )


@employee.get("", description="List all employees")
async def list_employees(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    try:
        employees, metadata = EmployeeCore.list_employees(pagination, db)
        return {"data": employees, "metadata": metadata}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while listing employees.",
        )


@employee.put("/{id}", response_model=EmployeeUpdateOut)
async def update_employee(
    id: int, data: EmployeeUpdate, db: Session = Depends(get_db)
):
    try:
        updated_employee = EmployeeCore.update_employee(id, data, db)
        if not updated_employee:
            raise HTTPException(status_code=404, detail="Employee not found.")
        return updated_employee
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while updating the employee.",
        )


@employee.delete("/{id}", response_model=EmployeeDeleteOut)
async def delete_employee(id: int, db: Session = Depends(get_db)):
    try:
        deleted_employee = EmployeeCore.delete_employee(id, db)
        if not deleted_employee:
            raise HTTPException(status_code=404, detail="Employee not found.")
        return EmployeeDeleteOut(message_id="employee_deleted_successfully")
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while deleting the employee.",
        )
