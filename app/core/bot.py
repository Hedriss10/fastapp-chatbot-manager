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

log = setup_logger()
STATUS_CODE = 201
import os

import httpx
from dotenv import load_dotenv

from app.core.messages import MessagesCore
from app.logs.log import setup_logger
from app.service.redis import SessionManager

load_dotenv()
URL_INSTANCE_EVOLUTION = os.getenv("URL_INSTANCE_EVOLUTION")
EVOLUTION_APIKEY = os.getenv("EVOLUTION_APIKEY")

log = setup_logger()
STATUS_CODE = 201


class BotCore:
    def __init__(
        self, message: str, sender_number: str, push_name: str, *args, **kwargs
    ):
        self.message_text = message.strip()
        self.sender_number = sender_number
        self.push_name = push_name
        self.base_url = URL_INSTANCE_EVOLUTION
        self.apikey = EVOLUTION_APIKEY
        self.session = SessionManager()

        self.message_handler = MessagesCore(
            message=self.message_text,
            sender_number=self.sender_number,
            push_name=self.push_name,
        )

    def _reset_session(self) -> str:
        try:
            keys_to_clear = [
                f"session:{self.sender_number}",
                f"{self.sender_number}_welcome",
                f"{self.sender_number}_employees_list",
                f"{self.sender_number}_products_list",
                f"{self.sender_number}_available_days",
                f"{self.sender_number}_selected_employee_id",
                f"{self.sender_number}_selected_product_id",
                f"{self.sender_number}_selected_day",
                f"{self.sender_number}_available_slots",
                f"{self.sender_number}_selected_slot",
                f"{self.sender_number}_state",
            ]
            for key in keys_to_clear:
                try:
                    self.session.delete(key)
                except Exception as ex:
                    print(f"WARNING: Could not delete key {key}: {ex}")

            return (
                "⚠️ Sua sessão foi reiniciada.\n"
                "Envie qualquer mensagem para começar novamente. 👋"
            )
        except Exception:
            return "⚠️ Ocorreu um erro ao reiniciar sua sessão. Tente novamente mais tarde."

    def _fallback_response(self, msg: str) -> str:
        print(f"DEBUG: Sessão inconsistente com msg '{msg}', resetando...")
        return self._reset_session()

    def get_response(self) -> str:
        try:
            msg = self.message_text

            # Reset manual
            if msg.lower() in ["reset", "reiniciar"]:
                return self._reset_session()

            state = self.session.get_key(f"{self.sender_number}_state")

            if state is None:
                self.session.set_key(
                    f"{self.sender_number}_state", "INICIO", expire_seconds=300
                )
                return self.message_handler.send_welcome()

            if state == "INICIO":
                if msg == "1":
                    message, employees = (
                        self.message_handler.send_list_employee()
                    )
                    if not employees:
                        return "⚠️ Nenhum profissional disponível no momento."
                    self.session.set_key(
                        f"{self.sender_number}_employees_list", employees, 300
                    )
                    self.session.set_key(
                        f"{self.sender_number}_state",
                        "ESCOLHER_FUNCIONARIO",
                        300,
                    )
                    return message
                else:
                    return "Por favor, digite 1 para iniciar o agendamento."

            elif state == "ESCOLHER_FUNCIONARIO":
                employees = self.session.get_key(
                    f"{self.sender_number}_employees_list"
                )
                if employees and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(employees):
                        selected_employee = employees[idx]
                        self.session.set_key(
                            f"{self.sender_number}_selected_employee_id",
                            selected_employee["id"],
                            300,
                        )
                        message, products = (
                            self.message_handler.send_list_products_id(
                                employee_id=selected_employee["id"]
                            )
                        )
                        if not products:
                            return "⚠️ Nenhum produto disponível para este profissional."
                        self.session.set_key(
                            f"{self.sender_number}_products_list",
                            products,
                            300,
                        )
                        self.session.set_key(
                            f"{self.sender_number}_state",
                            "ESCOLHER_PRODUTO",
                            300,
                        )
                        return message
                return self._fallback_response(msg)

            elif state == "ESCOLHER_PRODUTO":
                products = self.session.get_key(
                    f"{self.sender_number}_products_list"
                )
                if products and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(products):
                        selected_product = products[idx]
                        self.session.set_key(
                            f"{self.sender_number}_selected_product_id",
                            selected_product["id"],
                            300,
                        )
                        message, days = (
                            self.message_handler.send_available_days()
                        )
                        if not days:
                            return "⚠️ Nenhum dia disponível no momento."
                        self.session.set_key(
                            f"{self.sender_number}_available_days", days, 300
                        )
                        self.session.set_key(
                            f"{self.sender_number}_state", "ESCOLHER_DIA", 300
                        )
                        return message
                return self._fallback_response(msg)

            elif state == "ESCOLHER_DIA":
                available_days = self.session.get_key(
                    f"{self.sender_number}_available_days"
                )
                if available_days and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(available_days):
                        selected_day = available_days[idx]
                        self.session.set_key(
                            f"{self.sender_number}_selected_day",
                            selected_day,
                            300,
                        )

                        employee_id = self.session.get_key(
                            f"{self.sender_number}_selected_employee_id"
                        )
                        product_id = self.session.get_key(
                            f"{self.sender_number}_selected_product_id"
                        )

                        message, slots = (
                            self.message_handler.send_available_slots(
                                employee_id, selected_day, product_id
                            )
                        )
                        if not slots:
                            return message

                        self.session.set_key(
                            f"{self.sender_number}_available_slots", slots, 300
                        )
                        self.session.set_key(
                            f"{self.sender_number}_state",
                            "ESCOLHER_HORARIO",
                            300,
                        )
                        return message
                return self._fallback_response(msg)

            elif state == "ESCOLHER_HORARIO":
                available_slots = self.session.get_key(
                    f"{self.sender_number}_available_slots"
                )
                if available_slots and msg.isdigit():
                    idx = int(msg) - 1
                    if 0 <= idx < len(available_slots):
                        selected_slot = available_slots[idx]
                        self.session.set_key(
                            f"{self.sender_number}_selected_slot",
                            selected_slot,
                            300,
                        )
                        self.session.set_key(
                            f"{self.sender_number}_state",
                            "CONFIRMAR_AGENDAMENTO",
                            300,
                        )
                        return f"⏰ Ótimo! Você escolheu o horário {selected_slot[0].strftime('%H:%M')} até {selected_slot[1].strftime('%H:%M')}. Deseja confirmar o agendamento? (sim/não)"
                return self._fallback_response(msg)

            return self.message_handler.send_welcome()

        except Exception as e:
            print(f"ERROR: Failed to generate response: {e}")
            return self._reset_session()

    def send_message(self):
        try:
            response_text = self.get_response()

            print("DEBUG: RESPONSE TEXT gerado:", response_text)

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

            if response.status_code != STATUS_CODE:
                print(
                    f"ERROR: Failed to send message to {self.sender_number}: {response.status_code}, {response.text}"
                )

            return response

        except Exception as e:
            print(f"ERROR: Failed to send message: {e}")
            return None
