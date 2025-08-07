# app/models/employee.py

from datetime import datetime
from typing import Any, Dict, List, Tuple

from passlib.context import CryptContext
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    func,
    select,
    text,
    update,
)
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.auth.auth import create_access_token
from app.db.db import Base
from app.logs.log import setup_logger
from app.schemas.employee import (
    EmployeeBase,
    EmployeeDeleteOut,
    EmployeeGetIdOut,
    EmployeeOut,
    EmployeeUpdate,
    EmployeeUpdateOut,
)
from app.schemas.login import LoginEmployee, LoginEmployeeOut
from app.schemas.pagination import BuildMetadata, PaginationParams
from app.utils.metadata import Metadata

log = setup_logger()


EMPLOYEE_FIELDS = [
    'username',
    'date_of_birth',
    'phone',
    'role',
]

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = {'schema': 'employee'}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    role: Mapped[str] = mapped_column(String(40), nullable=False)
    session_token: Mapped[str] = mapped_column(Text, nullable=True)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=True)
    updated_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_by: Mapped[int] = mapped_column(Integer, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"""{self.username} created employee_successfully"""

    @classmethod
    def get_login(cls, data: LoginEmployee, db: Session):
        try:
            employee = db.query(cls).filter(cls.phone == data.phone).first()
            if employee:
                access_token = create_access_token({'sub': str(employee.id)})
                return LoginEmployeeOut(
                    user={
                        'id': employee.id,
                        'username': employee.username,
                        'phone': employee.phone,
                        'role': employee.role,
                    },
                    access_token=access_token,
                    message_id='employee_logged_successfully',
                )
            return None
        except Exception as e:
            log.error(f'Logger: Error get_login: {e}')
            raise

    @classmethod
    def get_employee(cls, id: int, db: Session) -> Dict[str, Any]:
        try:
            employee = (
                db.query(cls)
                .filter(cls.id == id, cls.is_deleted == False)
                .first()
            )
            if not employee:
                return None

            return EmployeeGetIdOut(
                id=employee.id,
                username=employee.username,
                date_of_birth=employee.date_of_birth,
                phone=employee.phone,
                role=employee.role,
            )
        except Exception as e:
            log.error(f'Logger: Error get_employee: {e}')
            raise

    @classmethod
    def list_employees(
        cls, pagination_params: PaginationParams, db: Session
    ) -> Tuple[List[Dict[str, Any]], BuildMetadata]:
        try:
            stmt = select(
                cls.id,
                cls.username,
                cls.date_of_birth,
                cls.phone,
                cls.role,
            ).where(cls.is_deleted == False)

            # filtrar por nome
            if pagination_params.filter_by:
                filter_value = f'%{pagination_params.filter_by}%'
                try:
                    stmt = stmt.filter(
                        func.unaccent(cls.username).ilike(
                            func.unaccent(filter_value)
                        )
                    )
                except Exception:
                    stmt = stmt.filter(cls.username.ilike(filter_value))

            if pagination_params.order_by:
                try:
                    sort_column = getattr(cls, pagination_params.order_by)
                    sort_direction = (
                        pagination_params.sort_by or 'asc'
                    ).lower()
                    stmt = stmt.order_by(
                        sort_column.asc()
                        if sort_direction == 'asc'
                        else sort_column.desc()
                    )
                except Exception as e:
                    log.error(f'Logger: Error list_employees: {e}')
                    raise

            # total count
            total_count = db.execute(
                select(func.count(cls.id)).select_from(stmt.subquery())
            ).scalar()

            # Paginação
            paginated_stmt = stmt.offset(
                (pagination_params.current_page - 1)
                * pagination_params.rows_per_page
            ).limit(pagination_params.rows_per_page)

            result = db.execute(paginated_stmt).fetchall()

            metadata = BuildMetadata(
                total_count=total_count,
                current_page=pagination_params.current_page,
                rows_per_page=pagination_params.rows_per_page,
                total_pages=(total_count + pagination_params.rows_per_page - 1)
                // pagination_params.rows_per_page,
            )

            return Metadata(result).model_to_list(), metadata
        except Exception as e:
            log.error(f'Logger: Error list_employees: {e}')
            raise

    @classmethod
    def add_employee(cls, data: EmployeeBase, db: Session):
        try:
            hashed_password = pwd_context.hash(data.password)
            new_employee = cls(
                username=data.username,
                date_of_birth=data.date_of_birth,
                phone=data.phone,
                role=data.role,
                password=hashed_password,
            )
            db.add(new_employee)
            db.commit()
            db.refresh(new_employee)
            return EmployeeOut(
                message_id='employee_created_successfully',
            )
        except Exception as e:
            log.error(f'Logger: Error add_employee: {e}')
            raise

    @classmethod
    def update_employee(cls, id: int, data: EmployeeUpdate, db: Session):
        try:
            employee = db.query(cls).filter(cls.id == id).first()

            update_key = {}
            for key, value in data:
                if value is not None and key in EMPLOYEE_FIELDS:
                    if hasattr(employee, key):
                        setattr(employee, key, value)
                        update_key[key] = value

                    if key == 'password':
                        hashed_password = pwd_context.hash(value)
                        setattr(employee, key, hashed_password)
                        update_key[key] = hashed_password

            stmt = update(cls).where(cls.id == id).values(update_key)
            db.execute(stmt)
            db.commit()
            return EmployeeUpdateOut(
                message_id='employee_updated_successfully'
            )
        except Exception as e:
            log.error(f'Logger: Error update_employee: {e}')
            raise

    @classmethod
    def delete_employee(cls, id: int, db: Session):
        try:
            employee = db.query(cls).filter(cls.id == id).first()
            if not employee:
                return None

            employee.is_deleted = True
            employee.deleted_at = datetime.now()
            db.commit()
            return EmployeeDeleteOut(
                message_id='employee_deleted_successfully'
            )
        except Exception as e:
            log.error(f'Logger: Error delete_employee: {e}')
            raise


class ScheduleEmployee(Base):
    __tablename__ = 'schedule_employee'
    __table_args__ = (
        CheckConstraint(
            "weekday IN ('segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo')",
            name='schedule_employee_weekday_check',
        ),
        {'schema': 'time_recording'},
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('public.employee.id', ondelete='CASCADE'),
        nullable=False,
    )

    weekday: Mapped[str] = mapped_column(String(9), nullable=False)

    start_time: Mapped[datetime] = mapped_column(Time, nullable=False)
    lunch_start: Mapped[datetime] = mapped_column(Time)
    lunch_end: Mapped[datetime] = mapped_column(Time)
    end_time: Mapped[datetime] = mapped_column(Time)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP')
    )

    updated_at: Mapped[datetime] = mapped_column(DateTime)
    updated_by: Mapped[int] = mapped_column(Integer)
    deleted_at: Mapped[datetime] = mapped_column(DateTime)
    deleted_by: Mapped[int] = mapped_column(Integer)

    is_deleted: Mapped[bool] = mapped_column(
        Boolean, server_default=text('false'), nullable=False
    )
