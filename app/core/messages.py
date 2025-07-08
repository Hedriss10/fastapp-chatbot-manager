# app/core/messages.py

from sqlalchemy.orm import Session

from app.db.db import SessionLocal
from app.logs.log import setup_logger
from app.messages.employee import EmployeeCore
from app.messages.products import ProductsCore
from app.messages.schedule import ScheduleCore
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
                        slot[0].strftime("%H:%M") for slot in raw_slots
                    ]

                    slots_list_text = "\n".join(
                        [f"⏰ {h}" for h in formatted_slots]
                    )

                    finish_message = (
                        f"✅ Horários disponíveis:\n\n{slots_list_text}"
                    )
                else:
                    finish_message = "🗓️ Não há horários disponíveis para este dia. Tente outro dia."

                return finish_message, raw_slots
        except Exception as e:
            log.error(f"Error in send_available_slots: {e}")
            return (
                "⚠️ Erro ao buscar horários disponíveis. Tente novamente mais tarde.",
                [],
            )

    def send_resume_scheduling(self, employe: str, select_service: str, date_select: str, hour_select: str):
        try:
            with SessionLocal() as session_local:
                stmt = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).resume_scheduling(
                    employee=employe,
                    select_service=select_service,
                    date_select=date_select,
                    hour_select=hour_select
                )
                return stmt
        except Exception as e:
            log.error(
                f"Error messages core \
                list avaliable days {e}"
            )

    def send_check_service_employee(self):
        try:
            with SessionLocal() as session_local:
                stmt = ScheduleCore(
                    message=self.message,
                    sender_number=self.sender_number,
                    push_name=self.push_name,
                    db=session_local,
                ).check_service_employee(
                    profissional_escolhido="Douglas Santos",
                    data_escolhida="13/07",
                    horario_escolhido="14:30",
                )
                return stmt
        except Exception as e:
            log.error(
                f"Error messages core \
                list avaliable days {e}"
            )
