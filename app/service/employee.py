from sqlalchemy.ext.asyncio import AsyncSession

from app.core.log import setup_logger
from app.repositories.employee_repositories import EmployeeRepositories
from app.schemas.employee import EmployeeBase, EmployeeOut

log = setup_logger()


class EmployeeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.employee_repo = EmployeeRepositories(session)

    async def add_employee(self, data: EmployeeBase):
        try:
            return await self.employee_repo.add_employee(data)
        except Exception as e:
            log.error(f'Error in add_employee: {e}')

    async def list_employee(self, pagination_params):
        try:
            return await self.employee_repo.list_employee(pagination_params)
        except Exception as e:
            log.error(f'Error in list_employee: {e}')

    async def get_employee(self, employee_id: int) -> EmployeeOut:
        try:
            return await self.employee_repo.get_employee_by_id(employee_id)
        except Exception as e:
            log.error(f'Error in get_employee: {e}')

    async def update_employee(
        self, employee_id: int, data: EmployeeBase
    ) -> EmployeeOut:
        try:
            return await self.employee_repo.update_employee(employee_id, data)
        except Exception as e:
            log.error(f'Error in update_employee: {e}')

    async def delete_employee(self, employee_id: int):
        try:
            return await self.employee_repo.delete_employee(employee_id)
        except Exception as e:
            log.error(f'Error in delete_employee: {e}')
