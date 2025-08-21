# app/service/login.py

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.log import setup_logger
from app.repositories.login_repositories import LoginRepositories
from app.schemas.login import LoginEmployee, LoginUser

log = setup_logger()


class LoginService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.login_repository = LoginRepositories(session)

    async def login_user(self, data: LoginUser):
        return await self.login_repository.get_login(data)

    async def login_employee(self, data: LoginEmployee):
        return await self.login_repository.get_employee_login(data)
