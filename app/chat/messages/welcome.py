# app/core/welcome.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.messages import SummaryMessage

log = setup_logger()


WELCOME_SUMMARY = "welcome_summary"


class WelcomeCore:
    def __init__(self, db: Session):
        self.db = db

    def flow_welcome(self):
        try:
            stmt = select(
                SummaryMessage.id,
                SummaryMessage.ticket,
                SummaryMessage.message,
            ).where(
                SummaryMessage.ticket == WELCOME_SUMMARY,
                ~SummaryMessage.is_deleted,
            )
            result = self.db.execute(stmt).first()
            if result:
                _, _, message = result
                return message["text"]

        except Exception as e:
            log.error(f"Error flow_welcome: {e}")
            return None
