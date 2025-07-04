# app/core/user.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base import BaseCore
from app.models.user import User
from app.schemas.user import UserCreate


class UserCore(BaseCore[User, UserCreate]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_phone(self, phone: str):
        query = select(User.username, User.lastname).where(User.phone == phone)
        result = self.db.execute(query)
        return [{"username": r[0], "phone": r[1]} for r in result]


# if __name__ == "__main__":
#     with SessionLocal() as db:
#         user = UserCore(db).get_by_phone(phone="556194261245")
#         print("User coletado", user)
