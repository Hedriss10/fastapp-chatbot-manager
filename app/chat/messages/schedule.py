# app/messages/schedule.py

from datetime import date, datetime, time, timedelta
from typing import List, Tuple, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.logs.log import setup_logger
from app.models.campaign.messages import SummaryMessage
from app.models.employee.employee import Employee
from app.models.product.product import Products
from app.models.schedules.block import ScheduleBlock
from app.models.schedules.schedule import ScheduleService
from app.models.time_recording.time_recording import ScheduleEmployee
from app.models.users.users import User

log = setup_logger()

LIST_DATE = 'list_dates'
RESUME_SCHEDULING = 'resume_scheduling'
CHECK_SERVICE_EMPLOYEE = 'check_service_employee'
CONFIRM_SCHEDULE_EMPLOYEE = 'confirm_schedule_employee'


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
        self.user = User
        self.db = db

    def add_schedule(
        self,
        send_number: str,
        employee_id: int,
        date: str,
        time: str,
        product_id: int,
    ):
        try:
            user_id = self.user.get_by_id_user(
                send_number=send_number, db=self.db
            )

            datetime_str = f'{date} {time}'
            time_register = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            schedule = self.schedule.add_schedule(
                db=self.db,
                time_register=time_register,
                product_id=product_id,
                employee_id=employee_id,
                user_id=user_id,
            )
            self.db.commit()
            return schedule
        except Exception as e:
            log.error(f'Logger: Error in add schedule: {e}')
            self.db.rollback()

    def update_schedule(self, send_number: str) -> str:
        try:
            user_id = self.user.get_by_id_user(
                send_number=send_number, db=self.db
            )

            update = self.schedule.update_is_check(
                db=self.db, is_check=True, user_id=user_id
            )
            return update
        except Exception as e:
            log.error(f'Logger: Error in add schedule: {e}')
            self.db.rollback()

    def list_available_days(self) -> tuple[str, list[str]]:
        try:
            # base_date = datetime.now().date() + timedelta(days=1)
            base_date = datetime.now().date()

            days_available = []
            options_day = ''
            for idx in range(7):
                day = base_date + timedelta(days=idx)
                day_str = day.strftime(
                    '%Y-%m-%d'
                )  # formato seguro para salvar e manipular
                days_available.append(day_str)
                options_day += f'{idx + 1}️⃣ {day.strftime("%d/%m")}\n'

            stmt = select(self.message.message).where(
                self.message.ticket == LIST_DATE
            )
            result_message = self.db.execute(stmt).fetchone()

            if not result_message:
                return '⚠️ Nenhuma mensagem configurada para datas.', []

            message_format = result_message[0]['text'].format(
                datas=options_day.strip()
            )
            return message_format, days_available

        except Exception as e:
            log.error(f'Logger: error list available days {e}')
        return '⚠️ Erro ao listar datas. Tente novamente mais tarde.', []

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
                select_date = datetime.strptime(select_date, '%Y-%m-%d').date()
            except Exception:
                return []

        weekday_map = {
            0: 'segunda',
            1: 'terça',
            2: 'quarta',
            3: 'quinta',
            4: 'sexta',
            5: 'sábado',
            6: 'domingo',
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

    def resume_scheduling(
        self,
        product_id: int,
        employee_id: int,
        date_selected: str,
        hour_selected: str,
    ) -> str:
        try:
            product = (
                self.db.query(Products.description)
                .filter(Products.id == product_id)
                .scalar()
            )

            employee = (
                self.db.query(Employee.username)
                .filter(Employee.id == employee_id)
                .scalar()
            )

            stmt = select(self.message.message).where(
                self.message.ticket == RESUME_SCHEDULING
            )
            result_message = self.db.execute(stmt).fetchone()

            if not result_message:
                return '⚠️ Nenhuma mensagem configurada para resumo do agendamento.'

            message_formated = result_message[0]['text'].format(
                nome_cliente=self.push_name,
                profissional_escolhido=employee,
                servico_escolhido=product,
                data_escolhida=date_selected,
                horario_escolhido=hour_selected,
            )

            return message_formated

        except Exception as e:
            log.error(f'Logger: Error in resume_scheduling: {e}')
            return '⚠️ Erro ao montar resumo do agendamento. Tente novamente mais tarde.'

    def send_check_employee(
        self,
        employee_id: int,
        product_id: int,
        date_selected: str,
        hour_selected: str,
    ):
        try:
            phone_employee = (
                self.db.query(Employee.phone)
                .filter(Employee.id == employee_id)
                .scalar()
            )

            product = (
                self.db.query(Products.description)
                .filter(Products.id == product_id)
                .scalar()
            )

            # tem que enviar uma mensagem para o employee
            send_check = select(self.message.message).where(
                self.message.ticket == CONFIRM_SCHEDULE_EMPLOYEE
            )

            result = self.db.execute(send_check).fetchone()

            # mensagem formatada enviada para o funcionario
            send_check_formated = result[0]['text'].format(
                nome_cliente=self.push_name,
                servico_escolhido=product,
                data_escolhida=date_selected,
                horario_escolhido=hour_selected,
            )
            return phone_employee, send_check_formated

        except Exception as e:
            log.error(f'Logger: error: send check employee: {e}')
            return None

    def check_service_employee(
        self,
        employee_id: int,
        date_selected: str,
        hour_selected: str,
    ) -> str:
        try:
            employee = (
                self.db.query(Employee.username)
                .filter(Employee.id == employee_id)
                .scalar()
            )

            stmt = select(self.message.message).where(
                self.message.ticket == CHECK_SERVICE_EMPLOYEE
            )
            result = self.db.execute(stmt).fetchone()

            if not result:
                return '⚠️ Nenhuma mensagem configurada para confirmação do agendamento.'

            message_format = result[0]['text'].format(
                profissional_escolhido=employee,
                data_escolhida=date_selected,
                horario_escolhido=hour_selected,
            )
            return message_format

        except Exception as e:
            log.error(f'Logger: Error in check_service_employee: {e}')
            return '⚠️ Erro ao gerar mensagem de confirmação.'


# if __name__ == "__main__":
#     # Coletando o dict {'client_phone': '556194261245', 'employee_id': 29, 'date': '2025-07-10', 'time': '09:00', 'product_id': 12}
#     from app.db.db import SessionLocal

#     with SessionLocal() as session_local:
#         a = ScheduleCore(
#             message="Ola",
#             sender_number="556194261245",
#             push_name="Hedris Pereira",
#             db=session_local,
#         )
#         # a.add_schedule(
#         #     send_number="556194261245",
#         #     employee_id=29,
#         #     date="2025-07-10",
#         #     time="09:00",
#         #     product_id=12,
#         # )
#         a.update_schedule(
#             send_number="556194261245"
#         )
