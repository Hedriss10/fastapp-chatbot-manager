# app/core/login.py

from sqlalchemy.orm import Session
from app.schemas.login import LoginUser
from app.models.users.users import User
from app.logs.log import setup_logger

log = setup_logger()

class LoginCore:

    @staticmethod
    async def login_user(data: LoginUser, db: Session = Session()):
        return User.get_login(data, db)