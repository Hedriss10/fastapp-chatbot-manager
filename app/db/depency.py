# app/db/dependency.py

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import AsyncSessionLocal


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
