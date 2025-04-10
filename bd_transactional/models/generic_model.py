from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from databases.db import db
from typing import Dict, Any
import re

def camel_to_snake(name: str) -> str:
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()

class GenericModel(db.Model):
    __abstract__ = True

    @classmethod
    def from_db(cls, data: Dict[str, Any]) -> "GenericModel":
        data_snake_case = {camel_to_snake(k): v for k, v in data.items()}
        return cls(**data_snake_case)

    @classmethod
    def from_db_add(cls, data: Dict[str, Any]) -> "GenericModel":
        data_snake_case = {camel_to_snake(k): v for k, v in data.items()}
        return cls(**{**data_snake_case, 'id': 0})

    def as_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}