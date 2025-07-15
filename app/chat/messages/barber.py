# app/messages/barber.py

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.employee import Employee
from app.models.messages import SummaryMessage

log = setup_logger()

ASK_WHICH_BARBER = "ask_which_barber"
ASK_SUBJECT = "ask_subject"
CONNECTING_TO_BARBER = "connecting_to_barber"
FORWARD_TO_BARBER = "forward_to_barber"


class BarberCore:
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
        self.employee = Employee
        self.message_summary = SummaryMessage

    def get_barber_info(self):
        employees_stmt = select(
            self.employee.id,
            self.employee.username,
        ).where(~self.employee.is_deleted)

        result_employees = self.db.execute(employees_stmt).fetchall()

        employees_list = []
        options_employee = ""

        for idx, (emp_id, username) in enumerate(result_employees, start=1):
            employees_list.append({"id": emp_id, "name": username})
            options_employee += f"{idx}️⃣ {username}  \n"

        # Pega mensagem base do banco (com placeholders)
        message_stmt = select(self.message_summary.message).where(
            self.message_summary.ticket == ASK_WHICH_BARBER
        )

        result_message = self.db.execute(message_stmt).fetchone()

        # Substitui o nome do cliente e insere os nomes formatados
        message_format = result_message[0]["text"].format(
            nome_cliente=self.push_name,
            opcoes_funcionarios=options_employee.strip(),
        )

        return message_format, employees_list

    def get_aks_subject_barber_info(self):
        try:
            stmt = select(
                SummaryMessage.id,
                SummaryMessage.ticket,
                SummaryMessage.message,
            ).where(
                SummaryMessage.ticket == ASK_SUBJECT,
                ~SummaryMessage.is_deleted,
            )
            result = self.db.execute(stmt).first()
            if result:
                _, _, message = result
                return message["text"]

        except Exception as e:
            log.error(f"Error get ask subject barbe info: {e}")
            return None

    def get_connecting_to_barber_info(self, employee_id: int) -> Optional[int]:
        try:
            employees_stmt = select(
                self.employee.username,
            ).where(~self.employee.is_deleted, self.employee.id == employee_id)

            result_employees = self.db.execute(employees_stmt).first()

            stmt = select(
                SummaryMessage.ticket,
                SummaryMessage.message,
            ).where(SummaryMessage.ticket == CONNECTING_TO_BARBER)
            result = self.db.execute(stmt).fetchone()

            message_format = result[1]["text"].format(
                nome_cliente=self.push_name,
                barbeiro_desejado=result_employees[0],
            )
            return message_format
        except Exception as e:
            log.error(f"Error get connecting to barber info: {e}")
            return None

    def get_forward_to_barber_info(
        self, type_schedule: str, employee_id: int
    ) -> Optional[str]:
        try:
            employees_stmt = select(
                self.employee.username, self.employee.phone
            ).where(~self.employee.is_deleted, self.employee.id == employee_id)

            result_employees = self.db.execute(employees_stmt).first()

            stmt = select(
                SummaryMessage.ticket,
                SummaryMessage.message,
            ).where(
                SummaryMessage.ticket == FORWARD_TO_BARBER,
                ~SummaryMessage.is_deleted,
            )
            result = self.db.execute(stmt).first()

            message_format = result[1]["text"].format(
                nome_cliente=self.push_name,
                tipo_atendimento=type_schedule,
            )
            return message_format, result_employees[1]
        except Exception as e:
            log.error(f"Error get forward to barber info: {e}")
            return None
