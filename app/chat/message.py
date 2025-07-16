# app/core/messages.py

from typing import Optional

from sqlalchemy.orm import Session

from app.chat.messages.barber import BarberCore
from app.chat.messages.employee import EmployeeCore
from app.chat.messages.opening_hours import OpeningHoursCore
from app.chat.messages.products import ProductsCore
from app.chat.messages.raflle_promo import RafflePromoCore
from app.chat.messages.schedule import ScheduleCore
from app.chat.messages.users import UsersCore
from app.chat.messages.welcome import WelcomeCore
from app.db.db import SessionLocal
from app.logs.log import setup_logger
from app.utils.slots import get_emoji_number

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

    def send_welcome(self):
        try:
            with SessionLocal() as session_local:
                stmt = WelcomeCore(db=session_local).flow_welcome()
                return stmt
        except Exception as e:
            log.error(f"Error in processing send welcome {e}")

    def send_list_employee(self) -> tuple[str, list[dict]]:
        try:
            with SessionLocal() as session_local:
                message, employees = EmployeeCore(
                    push_name=self.push_name, db=session_local
                ).list_employee()
                return message, employees
        except Exception as e:
            log.error(f"Error messages core list employee {e}")
            return (
                "⚠️ Erro ao listar funcionários. Tente novamente mais tarde.",
                [],
            )

    def send_list_products_id(self, employee_id: int):
        try:
            with SessionLocal() as session_local:
                message, products = ProductsCore(
                    push_name=self.push_name,
                    message=self.message,
                    sender_number=self.sender_number,
                    db=session_local,
                ).list_products(employee_id=employee_id)
                return message, products

        except Exception as e:
            log.error(
                f"Error messages core \
                list products filter by id employee {e}"
            )
            return (
                "⚠️ Erro ao listar produtos.Tente novamente mais tarde.",
                [],
            )

    def send_available_days(self):
        try:
            with SessionLocal() as session_local:
                list_days_available, days = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).list_available_days()
                return list_days_available, days
        except Exception as e:
            log.error(f"Error messages core list available days {e}")
            return "⚠️ Erro ao listar datas. Tente novamente mais tarde.", []

    def send_available_slots(
        self, employee_id: int, data_escolhida: str, product_id: int
    ):
        try:
            with SessionLocal() as session_local:
                raw_slots = ScheduleCore(
                    db=session_local,
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                ).get_available_slots(
                    employee_id=employee_id,
                    select_date=data_escolhida,
                    product_id=product_id,
                )

                if raw_slots:
                    formatted_slots = [
                        f"{get_emoji_number(i + 1)} {slot[0].strftime('%H:%M')}"
                        for i, slot in enumerate(raw_slots)
                    ]

                    slots_list_text = "\n".join(formatted_slots)

                    finish_message = f"✅ Horários disponíveis:\n\n{slots_list_text}\n\nDigite o número do horário que deseja escolher 👇"
                else:
                    finish_message = "🗓️ Não há horários disponíveis para este dia. Tente outro dia."

                return finish_message, raw_slots
        except Exception as e:
            log.error(f"Error in send_available_slots: {e}")
            return (
                "⚠️ Erro ao buscar horários disponíveis. Tente novamente mais tarde.",
                [],
            )

    def send_resume_scheduling(
        self,
        employee_id: int,
        date_selected: str,
        hour_selected: str,
        product_id: int,
    ):
        try:
            with SessionLocal() as session_local:
                message_formated = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).resume_scheduling(
                    employee_id=employee_id,
                    date_selected=date_selected,
                    hour_selected=hour_selected,
                    product_id=product_id,
                )
                return message_formated
        except Exception as e:
            log.error(
                f"Error messages core \
                list avaliable days {e}"
            )

    def approved_service(
        self,
        employee_id: int,
        product_id: int,
        date_selected: str,
        hour_selected: str,
    ):
        try:
            with SessionLocal() as session_local:
                phone_employee, stmt = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).send_check_employee(
                    employee_id=employee_id,
                    product_id=product_id,
                    date_selected=date_selected,
                    hour_selected=hour_selected,
                )
                return phone_employee, stmt
        except Exception as e:
            log.error(
                f"Error messages core \
                list avaliable days {e}"
            )

    def send_check_service_employee(
        self, employee_id: int, date_selected: str, hour_selected: str
    ):
        try:
            with SessionLocal() as session_local:
                stmt = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).check_service_employee(
                    employee_id=employee_id,
                    date_selected=date_selected,
                    hour_selected=hour_selected,
                )
                return stmt
        except Exception as e:
            log.error(
                f"Error messages core \
                list avaliable days {e}"
            )

    def send_add_schedule(
        self,
        send_number: str,
        employee_id: int,
        date: str,
        time: str,
        product_id: int,
    ):
        try:
            with SessionLocal() as session_local:
                stmt = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).add_schedule(
                    send_number=send_number,
                    employee_id=employee_id,
                    date=date,
                    time=time,
                    product_id=product_id,
                )
                return stmt

        except Exception as e:
            log.error(
                f"Error messages core \
                add schedule {e}"
            )

    def send_update_schedule(self, send_number: str) -> str:
        try:
            with SessionLocal() as session_local:
                stmt = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).update_schedule(
                    send_number=send_number,
                )
                return stmt

        except Exception as e:
            log.error(
                f"Error messages core \
                add update {e}"
            )

    def send_opening_hours(self) -> str:
        try:
            with SessionLocal() as session_local:
                stmt = OpeningHoursCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).flow_opening_hours()
                return stmt
        except Exception as e:
            log.error(f"Error messages core opening hours {e}")
            return "⚠️ Erro ao listar horários de funcionamento. Tente novamente mais tarde."

    def send_barber_info(self) -> tuple[str, list[dict]]:
        try:
            with SessionLocal() as session_local:
                message, employees = BarberCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).get_barber_info()
                return message, employees
        except Exception as e:
            log.error(f"Error messages core barber info {e}")
            return (
                "⚠️ Erro ao obter informações do barbeiro. Tente novamente mais tarde.",
                [],
            )

    def send_ask_subject(self) -> str:
        try:
            with SessionLocal() as session_local:
                stmt = BarberCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).get_aks_subject_barber_info()
                return stmt
        except Exception as e:
            log.error(f"Error messages core ask subject {e}")
            return "⚠️ Erro ao obter informações do assunto. Tente novamente mais tarde."
        return "Erro desconhecido ao obter informações do assunto."

    def send_connecting_to_barber(self, employee_id: int) -> Optional[int]:
        try:
            with SessionLocal() as session_local:
                stmt = BarberCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).get_connecting_to_barber_info(employee_id=employee_id)
                return stmt
        except Exception as e:
            log.error(f"Error messages core ask subject {e}")
            return "⚠️ Erro ao obter informações do assunto. Tente novamente mais tarde."
        return "Erro desconhecido ao obter informações do assunto."

    def send_forward_to_barber(
        self, type_schedule: str, employee_id: int
    ) -> Optional[str]:
        try:
            with SessionLocal() as session_local:
                stmt, emploee_phone = BarberCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).get_forward_to_barber_info(
                    type_schedule=type_schedule, employee_id=employee_id
                )
                return stmt, emploee_phone
        except Exception as e:
            log.error(f"Error messages core forward to barber {e}")
            return "⚠️ Erro ao encaminhar para o barbeiro. Tente novamente mais tarde."
        return "Erro desconhecido ao encaminhar para o barbeiro."

    def send_raffle_promo_info(self) -> str:
        try:
            with SessionLocal() as session_local:
                stmt = RafflePromoCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).get_raffle_promo_info()
                return stmt
        except Exception as e:
            log.error(f"Error messages core raffle promo info {e}")
            return "⚠️ Erro ao obter informações da promoção. Tente novamente mais tarde."
        return "Erro desconhecido ao obter informações da promoção."

    def send_check_existing_user(self) -> bool:
        try:
            with SessionLocal() as session_local:
                user_id = UsersCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).check_user_exists()
                return user_id
        except Exception as e:
            log.error(f"Error messages core check existing user {e}")
            return None

    def send_add_user(self, lastname: str) -> str:
        try:
            with SessionLocal() as session_local:
                stmt = UsersCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).add_users(lastname=lastname)
                return stmt
        except Exception as e:
            log.error(f"Error messages core add user {e}")
            return "⚠️ Erro ao adicionar usuário. Tente novamente mais tarde."
