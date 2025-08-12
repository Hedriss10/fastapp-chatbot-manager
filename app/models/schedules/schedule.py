from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger
from app.schemas.schedule import ScheduleInSchema, ScheduleOutSchema

log = setup_logger()


class ScheduleService(Base):
    __tablename__ = 'schedule'
    __table_args__ = {'schema': 'service'}

    id: Mapped[int] = mapped_column(primary_key=True)
    time_register: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_check: Mapped[int] = mapped_column(Boolean, nullable=False)
    is_awayalone: Mapped[int] = mapped_column(Boolean, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"""{self.id} created successfully"""

    @classmethod
    def add_schedule(
        cls,
        db: Session,
        time_register: datetime,
        product_id: int,
        employee_id: int,
        user_id: int,
        is_check: bool = False,
        is_awayalone: bool = False,
    ) -> Optional['ScheduleService']:
        try:
            schedule = cls(
                time_register=time_register,
                product_id=product_id,
                employee_id=employee_id,
                user_id=user_id,
                is_check=is_check,
                is_awayalone=is_awayalone,
                is_deleted=False,
                created_at=datetime.now(),
            )
            db.add(schedule)
            return schedule
        except Exception as e:
            log.error(f'Logger: Error add_schedule: {e}')
            return None

    @classmethod
    def update_is_check(
        cls, db: Session, is_check: bool, user_id: int
    ) -> Optional['ScheduleService']:
        try:
            schedule = (
                db.query(cls)
                .where(
                    cls.is_deleted == False,
                    cls.is_check == False,
                    cls.user_id == user_id,
                )
                .first()
            )
            if not schedule:
                log.warning('Logger: not_found_user_in_schedule')

            schedule.is_check = is_check
            schedule.updated_at = datetime.now()

            db.commit()
            db.refresh(schedule)

            return schedule
        except Exception as e:
            db.rollback()
            log.error(f'Logger: Error update_schedule: {e}')
            return None

    @classmethod
    def register_schedule(
        cls,
        data: ScheduleInSchema,
        db: Session,
    ):
        try:
            schedule = cls(
                time_register=data.time_register,
                product_id=data.product_id,
                employee_id=data.employee_id,
                user_id=data.user_id,
                is_check=False,
                is_awayalone=False,
                is_deleted=False,
                created_at=datetime.now(),
            )
            db.add(schedule)
            db.commit()
            return ScheduleOutSchema(
                message_id='schedule_created_successfully'
            )
        except Exception as e:
            db.rollback()
            log.error(f'Logger: Error add_schedule: {e}')
            raise

    @classmethod
    def get_schedule(cls): ...

    @classmethod
    def update_schedule(cls): ...

    @classmethod
    def delete_schedule(cls): ...
