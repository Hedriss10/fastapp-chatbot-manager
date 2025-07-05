# app/core/bot.py
import os

import httpx
from dotenv import load_dotenv

from app.core.messages import MessagesCore
from app.logs.log import setup_logger
from app.service.redis import SessionManager

load_dotenv()
URL_INSTANCE_EVOLUTION = os.getenv("URL_INSTANCE_EVOLUTION")
EVOLUTION_APIKEY = os.getenv("EVOLUTION_APIKEY")


logs = setup_logger()


class BotCore:
    def __init__(
        self, message: str, sender_number: str, push_name: str, *args, **kwargs
    ):
        self.message = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.base_url = URL_INSTANCE_EVOLUTION
        self.apikey = EVOLUTION_APIKEY
        self.session = SessionManager()
        self.message = MessagesCore(
            message=message, sender_number=sender_number, push_name=push_name
        )

    def _reset_session(self) -> str:
        try:
            keys_to_clear = [
                f"session:{self.sender_number}",
                f"{self.sender_number}_selected_period",
                f"{self.sender_number}_slots",
                f"{self.sender_number}_scheduler_state",
                f"{self.sender_number}_employee_id",
            ]
            for key in keys_to_clear:
                self.session.delete(key)
                print(f"DEBUG: Cleared Redis key {key}")
            print(f"INFO: Session reset for {self.sender_number}")
            # return RESPONSE_DICTIONARY["default"]
        except Exception as e:
            print(
                f"ERROR: Failed to reset session for {self.sender_number}: {e}"
            )
            # return RESPONSE_DICTIONARY["default"]

    def _handle_state_flow(self, state: str) -> str:
        state_handlers = {
            "welcome": self.message.send_welcome(),
        }
        for handler_state, handler in state_handlers.items():
            if state == handler_state or state.startswith(handler_state + ":"):
                try:
                    return handler()
                except Exception as e:
                    print(f"ERROR: Error handling state {state}: {e}")
                    return self._reset_session()
        print(f"WARNING: Unknown state {state} for {self.sender_number}")
        return self._reset_session()

    def get_response(self) -> str:
        try:
            self.message.send_welcome()
            # return self._reset_session()
            return self.message.send_welcome()
        except Exception as e:
            print(f"ERROR: Failed to generate response: {e}")
            return self._reset_session()

    def send_message(self):
        """
        Send a message to a recipient.

        Args:
            self: The current instance of the BotCore class.
            message: The message to send.
            sender_number: The phone number of the recipient.
            push_name: The push name of the sender (optional).

        Returns:
            A response object from the request.
        """
        try:
            # response_text = self.get_response()
            response_text = self.get_response()
            print("Coletnado o erro do RESPONSE TEXT", response_text)
            payload = {
                "number": self.sender_number,
                "text": response_text,
                "delay": 2000,
            }
            headers = {
                "apikey": self.apikey,
                "Content-Type": "application/json",
            }
            print(f"DEBUG: Sending payload to {self.sender_number}: {payload}")
            response = httpx.post(
                url=self.base_url, json=payload, headers=headers, timeout=5
            )
            print(
                f"DEBUG: Sent message to {self.sender_number}: {response.status_code}, {response.text}"
            )
            if response.status_code != 201:
                print(
                    f"ERROR: Failed to send message to {self.sender_number}: {response.status_code}, {response.text}"
                )
            return response
        except Exception as e:
            print(f"ERROR: Failed to send message: {e}")
            return None
