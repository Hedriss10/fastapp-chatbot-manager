# app/routes/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import ValidationError
from fastapi.exceptions import HTTPException
from app.core.users import UserCore
from app.db.depency import get_db
from app.schemas.pagination import PaginationParams
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserOut,
    UserUpdateOut,
    UserDeleteOut,
)

users = APIRouter(prefix="/users", tags=["users"])


@users.post("", description="Create a new user", response_model=UserOut)
async def add_users(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserCore.add_users(data, db)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating the user.",
        )


@users.get("", description="List all users")
async def list_users(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    try:
        users, metadata = UserCore.list_users(pagination, db)
        return {"data": users, "metadata": metadata}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while getting the users.",
        )


@users.get("/{id}", description="Get user of id")
async def get_user(id: int, db: Session = Depends(get_db)):
    try:
        return UserCore.get_user(id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while getting the user.",
        )


@users.put(
    "/{id}", description="Update user of id", response_model=UserUpdateOut
)
async def update_user(
    id: int, data: UserUpdate, db: Session = Depends(get_db)
):
    try:
        return UserCore.update_users(id, data, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while updating the user.",
        )


@users.delete(
    "/{id}", description="Delete user of id", response_model=UserDeleteOut
)
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        return UserCore.delete_users(id, db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while deleting the user.",
        )
