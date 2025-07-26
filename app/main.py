from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.bot import bot
from app.routes.healtchek import heartcheck
from app.routes.users import users
from app.routes.login import login
from app.routes.employee import employee

app = FastAPI(title="Fastapp build platform manager", version="1.0.0")


# Lista de origens que podem acessar sua API
origins = [
    "http://localhost:5173",  # Vite frontend local
    "http://localhost:3000",  # Se você tiver outro frontend
    "http://127.0.0.1:5173",  # Também cobre esse caso
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee)
app.include_router(login)
app.include_router(users)
app.include_router(bot)
app.include_router(heartcheck)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
