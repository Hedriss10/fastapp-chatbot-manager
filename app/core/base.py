# app/core/base.py

from typing import Any, Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseCore(Generic[ModelType, CreateSchemaType]):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get_all(self) -> List[ModelType]:
        stmt = select(self.model)
        return self.db.execute(stmt).scalars().all()

    def get_by_id(self, item_id: int) -> Optional[ModelType]:
        return self.db.get(self.model, item_id)

    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        column = getattr(self.model, field)
        stmt = select(self.model).where(column == value)
        return self.db.execute(stmt).scalars().first()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.dict()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, item_id: int) -> bool:
        obj = self.get_by_id(item_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
