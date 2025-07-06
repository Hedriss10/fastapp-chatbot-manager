# app/messages/schedule.py

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.employee import Employee
from app.models.messages import SummaryMessage
from app.models.schedule import ScheduleBlock, ScheduleService

log = setup_logger()

LIST_DATE = "list_dates"


class ScheduleCore:
    def __init__(
        self,
        message: str,
        sender_number: str,
        push_name: str,
        db: Session,
        *args,
        **kwargs,
    ):
        self.messsage = message
        self.sender_number = sender_number
        self.push_name = push_name
        self.schedule = ScheduleService
        self.employee = Employee
        self.block = ScheduleBlock
        self.message = SummaryMessage
        self.db = db

    def list_available_days(self):
        try:
            base_date = datetime.now().date() + timedelta(days=7)

            options_day = ""
            for idx in range(3):
                dia = base_date + timedelta(days=idx)
                options_day += f"{idx + 1}️⃣ {dia.strftime('%d/%m')}\n"

            stmt = select(self.message.message).where(
                self.message.ticket == LIST_DATE
            )
            result_message = self.db.execute(stmt).fetchone()

            if not result_message:
                return "⚠️ Nenhuma mensagem configurada para datas."

            message_format = result_message[0]["text"].format(
                datas=options_day.strip()
            )
            return message_format

        except Exception as e:
            log.error(f"Logger: Error list dates {e}")
            return "⚠️ Erro ao listar datas disponíveis. Tente novamente mais tarde."

    def add_schedule(self):
        try:
            stmt = ...

        except Exception as e:
            log.error(f"Error add schedule: {e}")
            return None

    def list_schedule(self): ...

    def delete_schedule(self): ...
