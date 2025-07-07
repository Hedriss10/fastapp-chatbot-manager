# app/messages/employee.py

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

    def list_employee(self) -> tuple[str, list[dict]]:
        try:
            employees_stmt = select(
                self.employee.id,
                self.employee.username,
            ).where(~self.employee.is_deleted)

            result_employees = self.db.execute(employees_stmt).fetchall()

            employees_list = []
            options_employee = ""

            for idx, (emp_id, username) in enumerate(
                result_employees, start=1
            ):
                employees_list.append({"id": emp_id, "name": username})
                options_employee += f"{idx}️⃣ {username}  \n"

            # Pega mensagem base do banco (com placeholders)
            message_stmt = select(self.message_summary.message).where(
                self.message_summary.ticket == LIST_EMPLOYEE
            )
            result_message = self.db.execute(message_stmt).fetchone()

            # Substitui o nome do cliente e insere os nomes formatados
            message_format = result_message[0]["text"].format(
                nome_cliente=self.push_name,
                opcoes_funcionarios=options_employee.strip(),
            )

            return message_format, employees_list

        except Exception as e:
            log.error(f"Logger: Error list employees: {e}")
            return (
                "⚠️ Erro ao listar funcionários. Tente novamente mais tarde.",
                [],
            )
