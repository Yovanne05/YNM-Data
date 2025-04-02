from typing import Type, List, Any, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError
from databases.db import db
from sqlalchemy import inspect


class GenericService:
    def __init__(self, model_class: Type):
        self.model_class = model_class
        self.table_name = model_class.__tablename__

    def get_all(self) -> List[Any]:
        """Récupère tous les enregistrements"""
        try:
            return db.session.query(self.model_class).all()
        except SQLAlchemyError as e:
            raise Exception(f"Erreur lors de la récupération: {str(e)}")

    def get_by_id(self, id: int) -> Optional[Any]:
        """Récupère un enregistrement par son ID"""
        try:
            return db.session.query(self.model_class).get(id)
        except SQLAlchemyError as e:
            raise Exception(f"Erreur lors de la récupération: {str(e)}")

    def create(self, data: Dict[str, Any]) -> Any:
        """Crée un nouvel enregistrement"""
        try:
            obj = self.model_class(**data)
            db.session.add(obj)
            db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la création: {str(e)}")

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Any]:
        """Met à jour un enregistrement"""
        try:
            obj = db.session.query(self.model_class).get(id)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la mise à jour: {str(e)}")

    def delete(self, id: int) -> bool:
        """Supprime un enregistrement"""
        try:
            obj = db.session.query(self.model_class).get(id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la suppression: {str(e)}")

    def get_table_schema(self) -> Dict[str, Dict[str, Any]]:
        """Retourne le schéma complet de la table"""
        try:
            inspector = inspect(db.engine)
            columns = inspector.get_columns(self.table_name)

            schema = {}
            for col in columns:
                schema[col['name']] = {
                    'type': str(col['type']),
                    'nullable': col['nullable'],
                    'primary_key': col.get('primary_key', False),
                    'default': col.get('default')
                }
            return schema
        except Exception as e:
            raise Exception(f"Erreur récupération schéma: {str(e)}")

    def get_table_structure(self) -> Dict[str, List[str]]:
        """Retourne la structure de la table (noms des colonnes)"""
        try:
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns(self.table_name)]
            return {self.table_name: columns}
        except Exception as e:
            raise Exception(f"Erreur récupération structure: {str(e)}")

    def get_with_filters(self, filters: dict) -> List[Any]:
        """Récupère avec filtres avancés"""
        try:
            query = db.session.query(self.model_class)

            for filter_key, value in filters.items():
                if "__" in filter_key:
                    column, operator = filter_key.split("__")
                else:
                    column = filter_key
                    operator = "eq"

                column_attr = getattr(self.model_class, column, None)
                if column_attr is None:
                    continue

                if operator == "eq":
                    query = query.filter(column_attr == value)
                elif operator == "ne":
                    query = query.filter(column_attr != value)
                elif operator == "gt":
                    query = query.filter(column_attr > value)
                elif operator == "lt":
                    query = query.filter(column_attr < value)
                elif operator == "gte":
                    query = query.filter(column_attr >= value)
                elif operator == "lte":
                    query = query.filter(column_attr <= value)
                elif operator == "like":
                    query = query.filter(column_attr.like(f"%{value}%"))
                elif operator == "not_like":
                    query = query.filter(~column_attr.like(f"%{value}%"))

            return query.all()
        except Exception as e:
            raise Exception(f"Erreur lors du filtrage: {str(e)}")