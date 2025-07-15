# app/models/user.py

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, Text, func, insert, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger
from app.utils.metadata import Metadata

log = setup_logger()


USER_FIELDS = [
    "username",
    "lastname",
    "phone",
]

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)
    session_token: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"""{self.id} created successfully"""

    @classmethod
    def get_by_id_user(cls, send_number: int, db: Session) -> Optional[int]:
        try:
            user_id = db.query(cls.id).filter(cls.phone == send_number).first()
            return user_id.id if user_id else None
        except Exception as e:
            log.error(f"Logger: error in colect ID user{e}")
            return None

    @classmethod
    def get_user(cls, id: int, db: Session):
        try:
            stmt = select(cls).where(cls.id == id)
            result = db.execute(stmt).fetchall()
            return Metadata(result).model_to_list()
        except Exception as e:
            log.error(f"Logger: Error get_user: {e}")
            raise

    @classmethod
    def add_users(cls, data: dict, db: Session):
        try:
            stmt = insert(cls).values(
                username=data.get("username"),
                lastname=data.get("lastname"),
                phone=data.get("phone"),
            )
            db.execute(stmt)
            db.commit()
            return stmt
        except Exception as e:
            log.error(f"Logger: Error add_users: {e}")
            raise

    @classmethod
    def list_users(cls, pagination_params: str, db: Session):
        try:
            stmt = select(
                cls.id,
                cls.username,
                cls.lastname,
                cls.phone,
            ).where(~cls.is_deleted)

            if pagination_params.filter_by:
                filter_value = f"%{pagination_params.filter_by}%"
                try:
                    stmt = stmt.filter(
                        func.unaccent(cls.username).ilike(
                            func.unaccent(filter_value)
                        )
                    )
                except Exception:
                    stmt = stmt.filter(cls.username.ilike(filter_value))

            sort_column = getattr(cls, pagination_params.order_by, None)
            if sort_column:
                stmt = stmt.order_by(
                    sort_column.asc()
                    if pagination_params.sort_by == "asc"
                    else sort_column.desc()
                )

            total_count = db.execute(
                select(func.count()).select_from(stmt.subquery())
            ).scalar()

            paginated_stmt = stmt.offset(
                (pagination_params.current_page - 1)
                * pagination_params.rows_per_page
            ).limit(pagination_params.rows_per_page)
            
            result = db.execute(paginated_stmt).fetchall()
            metadata = cls.build_metadata(total_count, pagination_params)
            return (
                Metadata(result).model_to_list(),
                metadata
            ) # todo - adjust metdata
            
        except Exception as e:
            log.error(f"Logger: Error list_users: {e}")
            raise

    @classmethod
    def update_users(cls): ...

    @classmethod
    def delete_users(self): ...
