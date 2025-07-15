# app/core/user.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base import BaseCore
from app.logs.log import setup_logger
from app.models.users.user import User
from app.schemas.user import UserCreate

logger = setup_logger()


class UserCore(BaseCore[User, UserCreate]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_phone(self, phone: str):
        query = select(User.username, User.lastname).where(User.phone == phone)
        result = self.db.execute(query)
        return [{"username": r[0], "phone": r[1]} for r in result]

    def add_user(self, data: dict):
        try:
            user = User(**data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return [{"message": "user_created_successfully"}]
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {e}")
            return [{"message": str(e)}]
