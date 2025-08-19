# app/core/login.py

from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.employee.employee import Employee
from app.models.users.users import User
from app.schemas.login import LoginEmployee, LoginUser

log = setup_logger()


class LoginCore:

    def __init__(self, db: Session):
        self.db = db

    async def login_user(self, data: LoginUser):
        return await User.get_login(data, self.db)

    async def login_employee(self, data: LoginEmployee):
        return await Employee.get_login(data, self.db)
