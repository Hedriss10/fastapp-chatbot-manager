# app/messages/opening_hours.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.messages import SummaryMessage

log = setup_logger()


WORKING_HOURS_INFO = 'working_hours_info'


class OpeningHoursCore:
    def __init__(
        self,
        message: str,
        sender_number: str,
        push_name: str,
        db: Session,
        *args,
        **kwargs,
    ):
        self.message = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.db = db

    def flow_opening_hours(self):
        try:
            stmt = select(
                SummaryMessage.id,
                SummaryMessage.ticket,
                SummaryMessage.message,
            ).where(
                SummaryMessage.ticket == WORKING_HOURS_INFO,
                ~SummaryMessage.is_deleted,
            )
            result = self.db.execute(stmt).first()
            if result:
                _, _, message = result
                return message['text']

        except Exception as e:
            log.error(f'Error flow_opening_hours: {e}')
            return None
