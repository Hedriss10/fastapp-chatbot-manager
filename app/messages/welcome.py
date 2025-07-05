# app/core/welcome.py
import json
from sqlalchemy.orm import Session
from app.models.messages import SummaryMessage, MessageFlow
from sqlalchemy import select
from app.logs.log import setup_logger

log = setup_logger()

class WelcomeCore:
    def __init__(self, db: Session):
        self.db = db

    def flow_welcome(self):
        try:
            stmt = select(
                SummaryMessage.id,
                SummaryMessage.ticket,
                SummaryMessage.message
            ).where(
                SummaryMessage.is_deleted == False
            )
            result = self.db.execute(stmt)
            record = result.first()
            if record:
                id, ticket, message = record
                return {
                    "id": id,
                    "ticket": ticket,
                    "message": message
                }
            return None
        except Exception as e:
            log.error(f"Error flow_welcome: {e}")
            return None


# if __name__ == "__main__":
#     from app.db.db import SessionLocal

#     with SessionLocal() as session:
#         core = WelcomeCore(db=session)
#         print(core.flow_welcome())
