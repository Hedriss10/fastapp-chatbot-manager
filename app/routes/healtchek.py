# app/routes/healtchek.py


from fastapi import APIRouter, HTTPException
from app.logs.log import setup_logger

log = setup_logger()

heartcheck = APIRouter(prefix="/heartcheck", tags=["heartcheck"])


@heartcheck.get("/", description="heartcheck check system backend")
async def get_healtcheck():
    try:
        return {"status": "ok"}
    except HTTPException as e:
        raise e


