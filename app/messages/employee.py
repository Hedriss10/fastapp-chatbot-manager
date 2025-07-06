# app/messages/employee.py

# TODO - criar o mecanismo da agenda
# TODO - criar a listagem de funcionarios

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.employee import Employee
from app.models.messages import SummaryMessage

log = setup_logger()


LIST_EMPLOYEE = "select_barber"


class EmployeeCore:
    def __init__(self, push_name: str, db: Session):
        self.db = db
        self.push_name = push_name
        self.employee = Employee
        self.message_summary = SummaryMessage

    def list_employee(self):
        try:
            employees_stmt = select(
                self.employee.id,
                self.employee.username,
            ).where(~self.employee.is_deleted)

            result_employees = self.db.execute(employees_stmt).fetchall()

            options_employee = ""
            for idx, (id, username) in enumerate(result_employees, start=1):
                options_employee += f"{idx}️⃣ {username}  \n"

            message_stmt = select(self.message_summary.message).where(
                self.message_summary.ticket == LIST_EMPLOYEE
            )

            result_message = self.db.execute(message_stmt).fetchone()

            if not result_message:
                return "⚠️ Nenhuma mensagem configurada."

            template_dict = result_message[0]
            template_text = template_dict["text"]

            message_format = template_text.format(
                nome_cliente=self.push_name,
                opcoes_funcionarios=options_employee.strip(),
            )

            return message_format

        except Exception as e:
            log.error(f"Logger: Error list employees: {e}")
            return "⚠️ Erro ao listar funcionários. Tente novamente mais tarde."
