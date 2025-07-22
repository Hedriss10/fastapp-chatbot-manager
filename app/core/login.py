# app/core/login.py

from sqlalchemy.orm import Session
from app.schemas.login import LoginUser, LoginEmployee
from app.models.users.users import User
from app.models.employee import Employee
from app.logs.log import setup_logger

log = setup_logger()


class LoginCore:
    @staticmethod
    async def login_user(data: LoginUser, db: Session = Session()):
        return User.get_login(data, db)

    @staticmethod
    async def login_employee(data: LoginEmployee, db: Session = Session()):
        return Employee.get_login(data, db)
