from fastapi import FastAPI

from app.api.routes.employee import employee
from app.api.routes.login import login
from app.api.routes.product import prodcuts
from app.api.routes.schedule import schedule
from app.api.routes.service import service
from app.api.routes.users import users


def init_routers(app: FastAPI) -> None:
    """Register all application routers."""
    app.include_router(employee)
    app.include_router(login)
    app.include_router(users)
    app.include_router(prodcuts)
    app.include_router(schedule)
    app.include_router(service)


__all__ = ["init_routers"]
