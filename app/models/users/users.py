# app/models/user.py

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
    Text,
    func,
    insert,
    select,
    update,
)
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.db.db import Base
from app.logs.log import setup_logger
from app.schemas.pagination import BuildMetadata, PaginationParams
from app.schemas.user import (
    UserCreate,
    UserDeleteOut,
    UserOut,
    UserUpdate,
    UserUpdateOut,
)
from app.schemas.login import LoginUser, LoginUserOut
from app.utils.metadata import Metadata
from app.auth.auth import create_access_token

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
            raise

    @classmethod
    def get_login(cls, data: LoginUser, db: Session):
        try:
            user = db.query(cls).filter(cls.phone == data.phone).first()
            if user:
                access_token = create_access_token({"sub": str(user.id)})
                return LoginUserOut(
                    user={
                        "id": user.id,
                        "username": user.username,
                        "lastname": user.lastname,
                        "phone": user.phone,
                    },
                    access_token=access_token,
                    message_id="user_logged_successfully",
                )
            return None
        except Exception as e:
            log.error(f"Logger: Error get_login: {e}")
            raise

    @classmethod
    def get_user(cls, id: int, db: Session):
        try:
            stmt = select(
                cls.id, cls.username, cls.lastname, cls.session_token
            ).where(cls.id == id, cls.is_deleted == False)
            result = db.execute(stmt).fetchall()
            return Metadata(result).model_to_list()
        except Exception as e:
            log.error(f"Logger: Error get_user: {e}")
            raise

    @classmethod
    def add_users(cls, data: UserCreate, db: Session):
        try:
            stmt = (
                insert(cls)
                .values(
                    username=data.username,
                    lastname=data.lastname,
                    phone=data.phone,
                )
                .returning(cls.id)
            )
            result = db.execute(stmt)
            db.commit()
            user_id = result.scalar_one()
            return UserOut(
                id=user_id,
                username=data.username,
                lastname=data.lastname,
                phone=data.phone,
            )
        except Exception as e:
            log.error(f"Logger: Error add_users: {e}")
            raise

    @classmethod
    def list_users(
        cls, pagination_params: PaginationParams, db: Session
    ) -> Tuple[List[Dict[str, Any]], BuildMetadata]:
        try:
            stmt = select(
                cls.id,
                cls.username,
                cls.lastname,
                cls.phone,
            ).where(~cls.is_deleted)

            # Filtro por nome
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

            # Ordenação
            if pagination_params.order_by:
                try:
                    sort_column = getattr(cls, pagination_params.order_by)
                    sort_direction = (
                        pagination_params.sort_by or "asc"
                    ).lower()
                    stmt = stmt.order_by(
                        sort_column.asc()
                        if sort_direction == "asc"
                        else sort_column.desc()
                    )
                except AttributeError:
                    log.warning(
                        f"Logger: Campo de ordenação inválido: {pagination_params.order_by}"
                    )

            # Total de registros
            total_count = db.execute(
                select(func.count()).select_from(stmt.subquery())
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
            log.error(f"Logger: Error list_users: {e}")
            raise

    @classmethod
    def update_users(cls, id: int, data: UserUpdate, db: Session):
        try:
            user = db.query(cls).filter(cls.id == id).first()

            update_key = {}
            for key, value in data:
                if value is not None and key in USER_FIELDS:
                    if hasattr(user, key):
                        setattr(user, key, value)
                        update_key[key] = value

            stmt = update(cls).where(cls.id == id).values(update_key)
            db.execute(stmt)
            db.commit()
            return UserUpdateOut(message_id="user_updated_successfully")
        except Exception as e:
            log.error(f"Logger: Error update_users: {e}")
            raise

    @classmethod
    def delete_users(cls, id: int, db: Session):
        try:
            users = db.query(cls).filter(cls.id == id).first()
            users.is_deleted = True
            db.commit()
            return UserDeleteOut(message_id="user_deleted_successfully")
        except Exception as e:
            log.error(f"Logger: Error delete_users: {e}")
            raise
