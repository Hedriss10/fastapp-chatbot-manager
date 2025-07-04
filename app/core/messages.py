# app/core/messages.py

from app.db.db import Session


class MessagesCore:
    def __init__(self, db: Session):
        self.db = db
