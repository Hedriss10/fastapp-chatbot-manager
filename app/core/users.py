# app/core/users.py

from sqlalchemy.orm import Session

from app.models.users.users import User
from app.schemas.pagination import PaginationParams


class UserCore:
    @staticmethod
    def list_users(pagination: PaginationParams, db: Session):
        return User.list_users(pagination, db)
