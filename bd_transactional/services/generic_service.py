import json
import re
from typing import Type, List, Any, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import class_mapper
from bd_transactional.services.log_service import add_logs
from databases.db import db
from sqlalchemy import inspect


class GenericService:
    def __init__(self, model_class: Type):
        self.model_class = model_class
        self.table_name = model_class.__tablename__
        self.logs: List[str] = []

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

    def create_item(self, data: Dict[str, Any]) -> Any:
        """Crée un nouvel enregistrement avec validation complète"""
        try:
            self._validate_data(data)

            # Validation des types et formats (optionnelle)
            if hasattr(self.model_class, 'validation_schema'):
                schema = getattr(self.model_class, 'validation_schema')
                errors = {}

                for field, rules in schema.items():
                    if field in data:
                        expected_type = rules.get('type')
                        if expected_type and not isinstance(data[field], eval(expected_type)):
                            errors[field] = f"Doit être de type {expected_type}"

                        if 'maxlength' in rules and len(str(data[field])) > rules['maxlength']:
                            errors[field] = f"Ne doit pas dépasser {rules['maxlength']} caractères"

                        if 'regex' in rules and not re.match(rules['regex'], str(data[field])):
                            errors[field] = "Format invalide"

                if errors:
                    raise ValueError(json.dumps({"errors": errors}))

            item = self.model_class(**data)
            db.session.add(item)
            db.session.commit()
            return item

        except ValueError as ve:
            db.session.rollback()
            try:
                error_data = json.loads(str(ve))
                raise ValueError(json.dumps(error_data))
            except json.JSONDecodeError:
                raise ValueError(json.dumps({"errors": {"general": str(ve)}}))

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la création: {str(e)}")
    def _validate_data(self, data):
        """Validation des données métier"""
        required_fields = {
            column.name for column in self.model_class.__table__.columns
            if not column.nullable
               and not column.primary_key
               and column.default is None
               and column.server_default is None
        }

        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise ValueError(f"Champs requis manquants: {', '.join(missing_fields)}")

        if hasattr(self.model_class, 'validate'):
            self.model_class.validate(data)

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
        """Supprime un enregistrement avec cascade"""
        try:
            obj = db.session.query(self.model_class).get(id)

            if not obj:
                return False

            db.session.delete(obj)
            db.session.commit()
            return True

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

    def get_primary_key(self, item):
        """Récupère le nom de la colonne clé primaire"""
        mapper = class_mapper(self.model_class)
        primary_keys = mapper.primary_key
        if not primary_keys:
            raise ValueError("Aucune clé primaire définie pour ce modèle")
        return primary_keys[0].name

    def get_column_schema(self, column_name: str) -> Dict[str, Any]:
        """Version corrigée avec gestion robuste des colonnes ENUM"""
        try:
            if not hasattr(self.model_class, '__table__'):
                return {"error": "Model has no table representation"}

            column = getattr(self.model_class, column_name, None)
            if column is None:
                return {"error": f"Column {column_name} not found"}

            if hasattr(column, 'type'):
                type_info = {
                    "name": column_name,
                    "type": str(column.type),
                    "nullable": column.nullable
                }

                if hasattr(column.type, 'enums'):
                    type_info.update({
                        "type": "ENUM",
                        "values": column.type.enums
                    })

                return type_info

            return {"error": "Column type could not be determined"}

        except Exception as e:
            return {"error": str(e)}

    def get_enum_values(self, column_name: str) -> Optional[List[str]]:
        """Récupère les valeurs possibles pour une colonne ENUM"""
        try:
            column = self.model_class.__table__.columns.get(column_name)
            if column and hasattr(column.type, 'enums'):
                return column.type.enums
            return None
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des valeurs ENUM: {str(e)}")

    def add_log(self, action: str, status: str, details: str = ""):
        """Ajoute une entrée de log en français"""
        messages = {
            'CREATE': {
                'SUCCESS': f"Ajout réussi dans la table {self.table_name}",
                'FAILED': f"Échec d'ajout dans la table {self.table_name}"
            },
            'UPDATE': {
                'SUCCESS': f"Mise à jour réussie dans la table {self.table_name}",
                'FAILED': f"Échec de mise à jour dans la table {self.table_name}"
            },
            'DELETE': {
                'SUCCESS': f"Suppression réussie dans la table {self.table_name}",
                'FAILED': f"Échec de suppression dans la table {self.table_name}"
            }
        }

        message = messages.get(action, {}).get(status, "Action inconnue")
        if details:
            message += f" - Détails: {details}"
        add_logs(message)

