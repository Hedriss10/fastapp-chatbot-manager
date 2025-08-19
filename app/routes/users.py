# app/routes/users.py

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.users import UserCore
from app.db.depency import get_db
from app.schemas.pagination import PaginationParams
from app.schemas.user import (
    UserCreate,
    UserDeleteOut,
    UserOut,
    UserUpdate,
    UserUpdateOut,
)

users = APIRouter(prefix='/users', tags=['users'])


@users.post('', description='Create a new user', response_model=UserOut)
async def add_users(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserCore(db=db).add_users(data)
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while creating the user.',
        )


@users.get('', description='List all users')
async def list_users(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    try:
        users, metadata = UserCore(db=db).list_users(pagination)
        return {'data': users, 'metadata': metadata}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while getting the users.',
        )


@users.get('/{id}', description='Get user of id')
async def get_user(id: int, db: Session = Depends(get_db)):
    try:
        return UserCore(db=db).get_user(id)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while getting the user.',
        )


@users.put(
    '/{id}', description='Update user of id', response_model=UserUpdateOut
)
async def update_user(
    id: int, data: UserUpdate, db: Session = Depends(get_db)
):
    try:
        return UserCore(db=db).update_users(id, data)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while updating the user.',
        )


@users.delete(
    '/{id}', description='Delete user of id', response_model=UserDeleteOut
)
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        return UserCore(db=db).delete_users(id)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail='Something went wrong while deleting the user.',
        )
