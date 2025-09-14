import json

from sqlalchemy.engine.row import Row
from sqlalchemy.inspection import inspect

from app.core.exception.exceptions import DatabaseError


class Metadata:
    def __init__(self, objects):
        self.objects = objects

    def model_to_dict(self, obj=None):
        obj = obj or self.objects

        # Caso já seja um dicionário
        if isinstance(obj, dict):
            return obj

        # Caso seja resultado de SELECT (Row)
        if isinstance(obj, Row):
            return dict(obj._mapping)

        # Caso seja uma tupla simples, tenta converter manualmente
        if isinstance(obj, tuple):
            return {f'col_{i}': value for i, value in enumerate(obj)}

        # Caso seja uma instância ORM
        try:
            return {
                c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs
            }
        except Exception:
            raise ValueError(
                f'Não foi possível converter objeto: \
                {obj}. Tipo: {type(obj)}'
            )

    def model_to_list(self):
        if isinstance(self.objects, list):
            if all(isinstance(obj, dict) for obj in self.objects):
                return self.objects  # já é lista de dicts
            if all(isinstance(obj, Row) for obj in self.objects):
                return [dict(obj._mapping) for obj in self.objects]
            if all(isinstance(obj, tuple) for obj in self.objects):
                return [self.model_to_dict(obj) for obj in self.objects]
            # Lista mista ou ORM
            return [self.model_to_dict(obj) for obj in self.objects]

        elif self.objects:
            return [self.model_to_dict(self.objects)]
        return []

    def model_to_json(self):
        return json.dumps(self.model_to_list(), default=str)

    def model_instance_to_dict_get_id(self):
        if hasattr(self.objects, '__table__'):
            return {
                column.name: getattr(self.objects, column.name)
                for column in self.objects.__table__.columns
            }
        raise ValueError(
            'Objeto não possui __table__ para extração de colunas.'
        )

    def model_to_raw_dict(self):
        if isinstance(self.objects, dict):
            return self.objects
        elif hasattr(self.objects, '__dict__'):
            return {
                c: getattr(self.objects, c)
                for c in self.objects.__table__.columns.keys()
            }
        elif hasattr(self.objects, '_mapping'):
            return dict(self.objects._mapping)
        else:
            raise DatabaseError('Não foi possível converter objeto')
