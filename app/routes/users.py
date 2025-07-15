# app/routes/users.py

from fastapi import APIRouter, HTTPException
from app.schemas.pagination import PaginationParams
from app.core.users import UserCore
from app.db.depency import get_db
from app.db.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


users = APIRouter(prefix="/users", tags=["users"])

@users.get("/users", description="List all users")
async def list_users(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    users, metadata = UserCore.list_users(pagination, db)
    return {"data": users, "metadata": metadata}
