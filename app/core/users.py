# app/core/users.py

from sqlalchemy.orm import Session

from app.models.users.users import User
from app.schemas.pagination import PaginationParams
from app.schemas.user import UserCreate, UserUpdate


class UserCore:
    @staticmethod
    def add_users(data: UserCreate, db: Session):
        return User.add_users(data, db)

    @staticmethod
    def list_users(pagination: PaginationParams, db: Session):
        return User.list_users(pagination, db)

    @staticmethod
    def get_user(id: int, db: Session):
        return User.get_user(id, db)

    @staticmethod
    def update_users(id: int, data: UserUpdate, db: Session):
        return User.update_users(id, data, db)

    @staticmethod
    def delete_users(id: int, db: Session):
        return User.delete_users(id, db)
