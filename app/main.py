from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.bot import bot
from app.routes.employee import employee
from app.routes.healtchek import heartcheck
from app.routes.login import login
from app.routes.product import prodcuts
from app.routes.schedule import schedule
from app.routes.users import users
from app.settings.settings import settings

app = FastAPI(title='Fastapp build platform manager', version='1.0.0')


# Lista de origens que podem acessar sua API
origins = [
    f'{settings.url_frontend}',
    f'{settings.url_vite_frontend}',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(employee)
app.include_router(login)
app.include_router(users)
app.include_router(bot)
app.include_router(heartcheck)
app.include_router(prodcuts)
app.include_router(schedule)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app, host='0.0.0.0', port=8000, reload=True)


# TODO - ajusta a refatoração do produto, precisa altera a importação no bot
