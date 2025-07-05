# app/core/messages.py

from sqlalchemy.orm import Session

from app.db.db import SessionLocal
from app.logs.log import setup_logger
from app.messages.welcome import WelcomeCore

log = setup_logger()


class MessagesCore:
    def __init__(
        self,
        message: str,
        sender_number: str,
        push_name: str,
        db: Session = None,
        *args,
        **kwargs,
    ):
        self.db = db
        self.message = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.welcome = WelcomeCore(db=db)

    def send_welcome(self):
        """
            _send_welcome_
            Messenger function of sending the welcome.
            Also responsible for giving up the summary with the option.
        Returns:
            _type_: _summary_
        """
        try:
            with SessionLocal() as session_local:
                stmt = WelcomeCore(db=session_local).flow_welcome()
                print("COLETANDO O STMT", stmt)
                return stmt
        except Exception as e:
            log.error(f"Error in processing send welcome {e}")
