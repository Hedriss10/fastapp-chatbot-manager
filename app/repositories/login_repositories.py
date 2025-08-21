from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import create_access_token
from app.core.log import setup_logger
from app.models.employee import Employee
from app.models.users import User
from app.schemas.login import (
    LoginEmployee,
    LoginEmployeeOut,
    LoginUser,
    LoginUserOut,
)

log = setup_logger()


class LoginRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = User
        self.employee = Employee

    async def get_login(self, data: LoginUser) -> Optional[LoginUserOut]:
        try:
            user = await self.session.execute(
                select(self.user).where(self.user.phone == data.phone)
            )
            user = user.scalar_one_or_none()
            if user:
                access_token = create_access_token({'sub': str(user.id)})
                return LoginUserOut(
                    user={
                        'id': user.id,
                        'username': user.username,
                        'lastname': user.lastname,
                        'phone': user.phone,
                    },
                    access_token=access_token,
                    message_id='user_logged_successfully',
                )
            return None
        except Exception as e:
            log.error(f'Logger: Error get_login: {e}')
            raise

    async def get_employee_login(
        self, data: LoginEmployee
    ) -> Optional[LoginEmployeeOut]:
        try:
            employee = await self.session.execute(
                select(self.employee).where(self.employee.phone == data.phone)
            )
            employee = employee.scalar_one_or_none()
            if employee:
                access_token = create_access_token({'sub': str(employee.id)})
                return LoginEmployeeOut(
                    user={
                        'id': employee.id,
                        'username': employee.username,
                        'phone': employee.phone,
                        'role': employee.role,
                    },
                    access_token=access_token,
                    message_id='employee_logged_successfully',
                )
            return None
        except Exception as e:
            log.error(f'Logger: Error get_employee_login: {e}')
            raise
