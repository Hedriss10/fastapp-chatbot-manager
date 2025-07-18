# app/routes/login.py


from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.login import LoginCore
from app.db.depency import get_db
from app.schemas.login import LoginUserOut, LoginUser


login = APIRouter(prefix="/login", tags=["login"])


@login.post("", response_model=LoginUserOut)
async def login_users(data: LoginUser, db: Session = Depends(get_db)):
    user = await LoginCore.login_user(data, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


# async def login_employees(): ...