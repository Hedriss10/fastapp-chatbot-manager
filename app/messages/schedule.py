# app/messages/schedule.py

from datetime import date, datetime, time, timedelta
from typing import List, Tuple, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.employee import Employee
from app.models.messages import SummaryMessage
from app.models.product import Products
from app.models.schedule import ScheduleBlock, ScheduleService
from app.models.time_recording import ScheduleEmployee

log = setup_logger()

LIST_DATE = "list_dates"
RESUME_SCHEDULING = "resume_scheduling"
CHECK_SERVICE_EMPLOYEE = "check_service_employee"


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

    def list_available_days(self) -> tuple[str, list[str]]:
        try:
            base_date = datetime.now().date() + timedelta(days=1)

            days_available = []
            options_day = ""
            for idx in range(7):
                day = base_date + timedelta(days=idx)
                day_str = day.strftime(
                    "%Y-%m-%d"
                )  # formato seguro para salvar e manipular
                days_available.append(day_str)
                options_day += f"{idx + 1}️⃣ {day.strftime('%d/%m')}\n"

            stmt = select(self.message.message).where(
                self.message.ticket == LIST_DATE
            )
            result_message = self.db.execute(stmt).fetchone()

            if not result_message:
                return "⚠️ Nenhuma mensagem configurada para datas.", []

            message_format = result_message[0]["text"].format(
                datas=options_day.strip()
            )

            return message_format, days_available

        except Exception as e:
            log.error(f"Logger: error list available days {e}")
        return "⚠️ Erro ao listar datas. Tente novamente mais tarde.", []

    def generator_interval(
        self, start: datetime, finish: datetime, delta_minutes: int = 20
    ) -> List[Tuple[datetime, datetime]]:
        """Gera lista de intervalos de tempo entre início e fim com delta_minutos de duração."""
        interval = []
        cursor = start
        try:
            delta = timedelta(minutes=delta_minutes)
        except Exception:
            raise
        while cursor + delta <= finish:
            interval.append((cursor, cursor + delta))
            cursor += delta
        return interval

    def get_available_slots(
        self,
        employee_id: int,
        select_date: Union[str, date],
        product_id: int,
    ) -> List[Tuple[datetime, datetime]]:
        if isinstance(select_date, str):
            try:
                select_date = datetime.strptime(select_date, "%Y-%m-%d").date()
            except Exception:
                return []

        weekday_map = {
            0: "segunda",
            1: "terça",
            2: "quarta",
            3: "quinta",
            4: "sexta",
            5: "sábado",
            6: "domingo",
        }
        weekday_str = weekday_map[select_date.weekday()]

        schedule_emp: ScheduleEmployee = (
            self.db.query(ScheduleEmployee)
            .filter(
                ScheduleEmployee.employee_id == employee_id,
                ScheduleEmployee.weekday == weekday_str,
                ScheduleEmployee.is_deleted == False,
            )
            .first()
        )
        if not schedule_emp:
            return []

        dt_start = datetime.combine(select_date, schedule_emp.start_time)
        dt_end = datetime.combine(select_date, schedule_emp.end_time)

        if schedule_emp.lunch_start and schedule_emp.lunch_end:
            lunch_start_dt = datetime.combine(
                select_date, schedule_emp.lunch_start
            )
            lunch_end_dt = datetime.combine(
                select_date, schedule_emp.lunch_end
            )
            intervals_before_lunch = self.generator_interval(
                start=dt_start, finish=lunch_start_dt
            )
            intervals_after_lunch = self.generator_interval(
                start=lunch_end_dt, finish=dt_end
            )
            work_intervals = intervals_before_lunch + intervals_after_lunch
        else:
            work_intervals = self.generator_interval(dt_start, dt_end)

        block_schedule: List[ScheduleBlock] = (
            self.db.query(ScheduleBlock)
            .filter(
                ScheduleBlock.employee_id == employee_id,
                ScheduleBlock.is_block == True,
                ScheduleBlock.is_deleted == False,
                ScheduleBlock.start_time
                >= datetime.combine(select_date, time.min),
                ScheduleBlock.start_time
                < datetime.combine(select_date + timedelta(days=1), time.min),
            )
            .all()
        )

        schedule_services: List[ScheduleService] = (
            self.db.query(ScheduleService)
            .filter(
                ScheduleService.employee_id == employee_id,
                ScheduleService.is_deleted == False,
                ScheduleService.time_register
                >= datetime.combine(select_date, time.min),
                ScheduleService.time_register
                < datetime.combine(select_date + timedelta(days=1), time.min),
            )
            .all()
        )
        prodcuts: Products = (
            self.db.query(Products)
            .filter(
                Products.id == product_id,
                Products.is_deleted == False,
            )
            .first()
        )
        if not prodcuts:
            return []

        duration_of_minutes = prodcuts.time_to_spend.total_seconds() / 60

        qtd_slots = int(duration_of_minutes // 20)
        if duration_of_minutes % 20 > 0:
            qtd_slots += 1

        slots_confirmedd = []

        for start_slot, fim_slot in work_intervals:
            slot_start = start_slot
            slot_end = slot_start + prodcuts.time_to_spend

            if slot_end > dt_end:
                continue

            conflict_schedule = any(
                not (
                    slot_end <= s.time_register
                    or slot_start >= s.time_register + prodcuts.time_to_spend
                )
                for s in schedule_services
            )
            has_block = any(
                not (slot_end <= b.start_time or slot_start >= b.end_time)
                for b in block_schedule
            )
            if has_block:
                continue

            if conflict_schedule:
                continue

            slots_confirmedd.append((slot_start, slot_end))
        return slots_confirmedd

    def add_schedule(self):
        # TODO - add schedule
        try:
            stmt = ...

        except Exception as e:
            log.error(f"Error add schedule: {e}")
            return None

    def list_schedule(self): ...

    def delete_schedule(self): ...

    def resume_scheduling(
        self,
        employee: str,
        select_service: str,
        date_select: str,
        hour_select: str,
    ) -> str:
        try:
            # Buscar template do banco
            stmt = select(self.message.message).where(
                self.message.ticket == RESUME_SCHEDULING
            )
            result_message = self.db.execute(stmt).fetchone()

            if not result_message:
                return "⚠️ Nenhuma mensagem configurada para resumo do agendamento."

            message_formated = result_message[0]["text"].format(
                nome_cliente=self.push_name,
                profissional_escolhido=employee,
                servico_escolhido=select_service,
                data_escolhida=date_select,
                horario_escolhido=hour_select,
            )

            return message_formated

        except Exception as e:
            log.error(f"Logger: Error in resume_scheduling: {e}")
            return "⚠️ Erro ao montar resumo do agendamento. Tente novamente mais tarde."

    def check_service_employee(
        self,
        employee_select: str,
        date_select: str,
        hour_select: str,
    ) -> str:
        try:
            # Buscar template no banco
            stmt = select(self.message.message).where(
                self.message.ticket == CHECK_SERVICE_EMPLOYEE
            )
            result_message = self.db.execute(stmt).fetchone()

            if not result_message:
                return "⚠️ Nenhuma mensagem configurada para confirmação do agendamento."

            template_dict = result_message[0]
            template_text = template_dict["text"]

            message_format = template_text.format(
                profissional_escolhido=employee_select,
                data_escolhida=date_select,
                horario_escolhido=hour_select,
            )

            return message_format

        except Exception as e:
            log.error(f"Logger: Error in check_service_employee: {e}")
            return "⚠️ Erro ao gerar mensagem de confirmação."
