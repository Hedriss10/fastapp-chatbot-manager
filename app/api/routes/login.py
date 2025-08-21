# app/routes/login.py

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.depency import get_db
from app.schemas.login import (
    LoginEmployee,
    LoginEmployeeOut,
    LoginUser,
    LoginUserOut,
)
from app.service.login import LoginService

login = APIRouter(prefix='/login', tags=['login'])


@login.post('', response_model=LoginUserOut, description='Login user')
async def login_users(data: LoginUser, db: AsyncSession = Depends(get_db)):
    user = await LoginService(session=db).login_user(data)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return user


@login.post(
    '/employee', response_model=LoginEmployeeOut, description='Login employee'
)
async def login_employee(
    data: LoginEmployee, db: AsyncSession = Depends(get_db)
):
    user = await LoginService(session=db).login_employee(data)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return user
