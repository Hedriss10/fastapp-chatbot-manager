from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

metadata_obj = MetaData(naming_convention=naming_convention)
# metadata_obj = MetaData(schema="public",
#   naming_convention=naming_convention)


class Base(DeclarativeBase):
    metadata = metadata_obj


__all__ = ('Base',)
