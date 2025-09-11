import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import init_routers

app = FastAPI(title='FastAPI - Build Barbershop', version='1.0.1')


origins = os.getenv('CORS_ORIGINS', '').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# init routes from routers
init_routers(app)

static_dir = os.path.join(os.path.dirname(__file__), 'static')


# static_dir = Path(__file__).parent / 'static'
static_dir = Path(__file__).parent / 'app' / 'static'
if static_dir.exists():
    app.mount('/static', StaticFiles(directory=static_dir), name='static')
else:
    print(f'[WARNING] Static folder not found at {static_dir}')


app.mount('/static', StaticFiles(directory=static_dir), name='static')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app=app, host='0.0.0.0', port=8000, reload=True)
