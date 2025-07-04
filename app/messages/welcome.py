# app/core/welcome.py

from app.db.db import Session


class WelcomeCore:
    def __init__(self, db: Session):
        self.db = db
        
    def flow_welcome(self):
        ...