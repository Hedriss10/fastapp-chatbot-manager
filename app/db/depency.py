# app/db/depency.py

from sqlalchemy.orm import Session
from app.db.db import SessionLocal


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
