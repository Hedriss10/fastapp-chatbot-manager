# app/core/messages.py

from sqlalchemy.orm import Session
from app.messages.welcome import WelcomeCore
from logs.log import setup_logger
from app.schemas.messages import ManagerMesssages

log = setup_logger()

class MessagesCore:
    
    def __init__(self, ManagerMesssages):
        self.welcome = WelcomeCore
        
    def send_welcome(self):
        try:
            return self.welcome.flow_welcome()
        except Exception as e:
            log.error(f"Error in processing send welcome {e}")
