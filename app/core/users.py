# app/core/users.py

from sqlalchemy.orm import Session

from app.models.users.users import User
from app.schemas.pagination import PaginationParams
from app.schemas.user import UserCreate, UserUpdate


class UserCore:
    def __init__(self, db: Session):
        self.db = db

    def add_users(self, data: UserCreate):
        return User.add_users(data, self.db)

    def list_users(self,pagination: PaginationParams):
        return User.list_users(pagination, self.db)

    def get_user(self, id: int):
        return User.get_user(id, self.db)

    def update_users(self, id: int, data: UserUpdate):
        return User.update_users(id, data, self.db)

    @staticmethod
    def delete_users(self, id: int):
        return User.delete_users(id, self.db)
