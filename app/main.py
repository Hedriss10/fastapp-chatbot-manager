from fastapi import FastAPI
from app.routes.bot import bot

app = FastAPI(title="Fastapp build chatbot manager", version="0.0.1")
app.include_router(bot)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
