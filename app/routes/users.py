# app/routes/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.users import UserCore
from app.db.depency import get_db
from app.schemas.pagination import PaginationParams

users = APIRouter(prefix="/users", tags=["users"])


@users.get("", description="List all users")
async def list_users(
    pagination: PaginationParams = Depends(), db: Session = Depends(get_db)
):
    users, metadata = UserCore.list_users(pagination, db)
    return {"data": users, "metadata": metadata}
