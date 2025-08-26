import os

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes.bot import bot
from app.api.routes.employee import employee
from app.api.routes.login import login
from app.api.routes.product import prodcuts
from app.api.routes.schedule import schedule
from app.api.routes.users import users
from app.settings.settings import settings

app = FastAPI(title='Fastapp build platform manager', version='1.0.0')


origins = [
    f'{settings.url_frontend}',
    f'{settings.url_vite_frontend}',
    f'{settings.cors_origins_}',
    f'{settings.cors_origins}',
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
app.include_router(prodcuts)
app.include_router(schedule)

static_dir = os.path.join(os.path.dirname(__file__), 'static')


static_dir = Path(__file__).parent / 'app' / 'static'
if static_dir.exists():
    app.mount('/static', StaticFiles(directory=static_dir), name='static')
else:
    print(f'[WARNING] Static folder not found at {static_dir}')


app.mount('/static', StaticFiles(directory=static_dir), name='static')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app, host='0.0.0.0', port=8000, reload=True)
