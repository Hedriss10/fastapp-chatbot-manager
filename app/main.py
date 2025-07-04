from fastapi import FastAPI

app = FastAPI(title="Fastapp build chatbot manager", version="1.0.0")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
