# app/core/bot.py
import os

import httpx
from dotenv import load_dotenv

from app.logs.log import setup_logger

load_dotenv()
URL_INSTANCE_EVOLUTION = os.getenv("URL_INSTANCE_EVOLUTION")
EVOLUTION_APIKEY = os.getenv("EVOLUTION_APIKEY")


logs = setup_logger()


class BotCore:
    def __init__(self, message: str, sender_number: str, push_name: str):
        self.message = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.base_url = URL_INSTANCE_EVOLUTION
        self.apikey = EVOLUTION_APIKEY

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
            response_text = "Issso é um teste do Software enginner Hedris"
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
