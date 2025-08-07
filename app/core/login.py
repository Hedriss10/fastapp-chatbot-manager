# app/core/login.py

from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.employee.employee import Employee
from app.models.users.users import User
from app.schemas.login import LoginEmployee, LoginUser

log = setup_logger()


class LoginCore:
    @staticmethod
    async def login_user(data: LoginUser, db: Session = Session()):
        return User.get_login(data, db)

    @staticmethod
    async def login_employee(data: LoginEmployee, db: Session = Session()):
        return Employee.get_login(data, db)
