# app/core/user.py

from sqlalchemy import select
from app.models.user import User
from typing import List
from app.db.db import Base as db

class UserCore:
    def __init__(self, *args, **kwargs):
        self.user = User
    
    def create_user(self, username: str, lastname: str, phone: str) -> User:
        return
    
    def read_user(self) -> List:
        try:
            stmt = select(
                self.user.username,
                self.user.lastname,
                self.user.phone
            )
            db.session.execute(stmt)
            
        except Exception as e:
            print("""Error list read users: {e}""")
