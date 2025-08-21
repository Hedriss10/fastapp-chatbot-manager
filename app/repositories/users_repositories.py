from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


class UserRepositories:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = User
