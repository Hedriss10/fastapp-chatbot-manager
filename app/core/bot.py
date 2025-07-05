# app/core/bot.py
import os

import httpx
from dotenv import load_dotenv

from app.logs.log import setup_logger
from app.service.redis import SessionManager

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
        self.session = SessionManager()


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
        """Gerencia o fluxo baseado no estado atual do usuário"""
        state_handlers = {
            "undefined": self._handle_registration,
            "awaiting_cancel_id": self._handle_cancellation,
            "awaiting_period_selection": self._handle_period_selection,
            "awaiting_time_slot": self._handle_time_slot_selection,
            "awaiting_employee": self.scheduler.handle_schedule,
            "awaiting_product": self.scheduler.handle_schedule,
            "awaiting_period": self._handle_period_selection,
            "awaiting_slot": self.scheduler.handle_schedule,
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
            if self.message == "menu":
                print(
                    f"DEBUG: User requested menu, resetting state for {self.sender_number}"
                )
                return self._reset_session()

            state = self.session.get(self.sender_number)
            print(f"DEBUG: Current state for {self.sender_number}: {state}")

            if state and state.startswith("awaiting_slot"):
                print(
                    f"DEBUG: Forcing session reset due to awaiting_slot state {state} for {self.sender_number}"
                )
                self._reset_session()
                state = None

            if state:
                return self._handle_state_flow(state)

            if self.message == "1":
                if not self.identify_user():
                    self.session.set(self.sender_number, "undefined")
                    print(
                        f"DEBUG: User not identified, set state to undefined for {self.sender_number}"
                    )
                    return "👥 Por favor, envie seu nome completo *(nome e sobrenome)*.\n\nDigite 'menu' para voltar ao início."
                self.session.set(self.sender_number, "undefined")
                print(
                    f"DEBUG: Set state to undefined for {self.sender_number}"
                )
                return self.scheduler.handle_schedule()

            elif self.message == "2":
                print(
                    f"DEBUG: User requested operating hours for {self.sender_number}"
                )
                return (
                    "🗓️⏱️👥 Nossos horários de atendimento são:\n"
                    "*Segunda a Sábado e Feriado*: 8h às 20h\n\n"
                    "*Domingo*: 8h às 18h\n\n"
                    "Para agendar, digite 1️⃣.\nDigite 'menu' para voltar ao início."
                )

            elif self.message == "3":
                self.session.set(self.sender_number, "awaiting_cancel_id")
                print(
                    f"DEBUG: Set state to awaiting_cancel_id for {self.sender_number}"
                )
                return self.scheduler.cancel_schedule()

            elif self.message == "4":
                print(
                    f"DEBUG: User requested their schedules for {self.sender_number}"
                )
                return self.scheduler.list_schedules()

            print(
                f"DEBUG: No valid option selected, resetting to default for {self.sender_number}"
            )
            return self._reset_session()
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
