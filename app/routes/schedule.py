# app/routes/schedule.py

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.users import UserCore
from app.db.depency import get_db
from app.schemas.pagination import PaginationParams

schedule = APIRouter(prefix='/schedule', tags=['schedule'])