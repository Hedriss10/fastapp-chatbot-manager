from fastapi import FastAPI

from app.routes.bot import bot
from app.routes.healtchek import heartcheck

app = FastAPI(title="Fastapp build platform manager", version="1.0.0")
app.include_router(bot)
app.include_router(heartcheck)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True)
