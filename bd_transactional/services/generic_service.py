import json
from typing import Type, List, Any, Dict, Optional
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import class_mapper

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

    def create_item(self, data):
        """Version robuste avec validation améliorée"""
        try:
            # Validation des types
            schema = {
                'nom': {'type': 'string', 'maxlength': 100},
                'date_debut': {'type': 'string', 'regex': r'^\d{4}-\d{2}-\d{2}$'},
                # Ajoutez tous les champs nécessaires
            }

            errors = {}
            for field, rules in schema.items():
                if field in data:
                    if not isinstance(data[field], str) and rules['type'] == 'string':
                        errors[field] = "Doit être une chaîne de caractères"
                    # Ajoutez d'autres règles de validation...

            if errors:
                raise ValueError(json.dumps({"errors": errors}))

            # Reste de la logique...
            item = self.model_class(**data)
            db.session.add(item)
            db.session.commit()
            return item

        except ValueError as ve:
            db.session.rollback()
            try:
                # Si l'erreur contient du JSON (validation structurée)
                error_data = json.loads(str(ve))
                raise ValueError(error_data)
            except json.JSONDecodeError:
                # Erreur texte simple
                raise ve

    def _validate_data(self, data):
        """Validation des données métier"""
        # 1. Vérifier les champs requis
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

        # 2. Validation spécifique au modèle
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
            # Charge l'objet avec toutes ses relations (ajustez selon vos besoins)
            obj = db.session.query(self.model_class).get(id)

            if not obj:
                return False

            db.session.delete(obj)  # Laisser SQLAlchemy gérer la cascade
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
            # Vérification de base
            if not hasattr(self.model_class, '__table__'):
                return {"error": "Model has no table representation"}

            # Récupération sécurisée de la colonne
            column = getattr(self.model_class, column_name, None)
            if column is None:
                return {"error": f"Column {column_name} not found"}

            # Pour les colonnes SQLAlchemy standard
            if hasattr(column, 'type'):
                type_info = {
                    "name": column_name,
                    "type": str(column.type),
                    "nullable": column.nullable
                }

                # Gestion spéciale des ENUM
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
