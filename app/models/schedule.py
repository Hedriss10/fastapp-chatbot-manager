# app/models/schedule.py

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger

log = setup_logger()


class ScheduleService(Base):
    __tablename__ = "service"
    __table_args__ = {"schema": "schedule"}

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
    ) -> Optional["ScheduleService"]:
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
            log.error(f"Logger: Error add_schedule: {e}")
            return None

    @classmethod
    def update_is_check(
        cls, db: Session, is_check: bool, user_id: int
    ) -> Optional["ScheduleService"]:
        try:
            schedule = db.query(cls).where(
                cls.is_deleted == False,
                cls.is_check == False,
                cls.user_id == user_id
            ).first()
            if not schedule:
                log.warning(f"Logger: not_found_user_in_schedule")
            
            schedule.is_check = is_check
            schedule.updated_at = datetime.now()
            
            db.commit()
            db.refresh(schedule)
            
            return schedule
        except Exception as e:
            db.rollback()
            log.error(f"Logger: Error update_schedule: {e}")
            return None


class ScheduleBlock(Base):
    __tablename__ = "block"
    __table_args__ = {"schema": "schedule"}

    id: Mapped[int] = mapped_column(primary_key=True)

    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)

    employee_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("public.employee.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("now()")
    )

    updated_at: Mapped[datetime] = mapped_column(DateTime)
    updated_by: Mapped[int] = mapped_column(Integer)
    deleted_at: Mapped[datetime] = mapped_column(DateTime)
    deleted_by: Mapped[int] = mapped_column(Integer)

    is_block: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), nullable=False
    )
