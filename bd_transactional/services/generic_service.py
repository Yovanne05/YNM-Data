import json
import re
from typing import Type, List, Any, Dict, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import class_mapper
from sqlalchemy import inspect, asc, desc

from bd_transactional.services.log_service import add_logs
from databases.db import db


class GenericService:
    """Service générique pour les opérations CRUD et de requêtage sur un modèle SQLAlchemy."""

    FILTER_OPERATORS = {
        'eq': lambda col, val: col == val,
        'ne': lambda col, val: col != val,
        'gt': lambda col, val: col > val,
        'lt': lambda col, val: col < val,
        'gte': lambda col, val: col >= val,
        'lte': lambda col, val: col <= val,
        'like': lambda col, val: col.like(f"%{val}%"),
        'not_like': lambda col, val: ~col.like(f"%{val}%")
    }

    def __init__(self, model_class: Type):
        """Initialise le service avec la classe du modèle."""
        self.model_class = model_class
        self.table_name = model_class.__tablename__
        self.logs: List[str] = []

    def get_all(self) -> List[Any]:
        """Récupère tous les enregistrements."""
        try:
            return db.session.query(self.model_class).all()
        except SQLAlchemyError as e:
            raise self._handle_db_error("réception", e)

    def get_by_id(self, id: int) -> Optional[Any]:
        """Récupère un enregistrement par son ID."""
        try:
            return db.session.query(self.model_class).get(id)
        except SQLAlchemyError as e:
            raise self._handle_db_error("réception", e)

    def create_item(self, data: Dict[str, Any]) -> Any:
        """Crée un nouvel enregistrement avec validation complète."""
        try:
            self._validate_data(data)
            self._validate_with_schema(data) if hasattr(self.model_class, 'validation_schema') else None

            item = self.model_class(**data)
            db.session.add(item)
            db.session.commit()
            return item
        except ValueError as ve:
            db.session.rollback()
            raise self._handle_validation_error(ve)
        except SQLAlchemyError as e:
            db.session.rollback()
            raise self._handle_db_error("création", e)

    def update(self, id: int, data: Dict[str, Any]) -> Optional[Any]:
        """Met à jour un enregistrement existant."""
        try:
            obj = self.get_by_id(id)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                db.session.commit()
            return obj
        except SQLAlchemyError as e:
            db.session.rollback()
            raise self._handle_db_error("mise à jour", e)

    def delete(self, identifier: Any) -> bool:
        """Supprime un enregistrement en gérant automatiquement les clés simples et composites"""
        try:
            # Récupère le schéma pour connaître la structure de la PK
            schema = self.get_table_schema()
            pk_columns = [col for col in schema if schema[col]['primary_key']]

            # Gestion des clés composites
            if len(pk_columns) > 1:
                if not isinstance(identifier, dict):
                    raise ValueError("Pour une clé composite, l'identifiant doit être un dictionnaire")

                # Vérifie que toutes les colonnes PK sont présentes
                missing = set(pk_columns) - set(identifier.keys())
                if missing:
                    raise ValueError(f"Clés primaires manquantes: {', '.join(missing)}")

                # Crée le tuple dans l'ordre des colonnes PK
                pk_values = tuple(identifier[col] for col in pk_columns)
                obj = db.session.query(self.model_class).get(pk_values)
            else:
                # Gestion classique pour clé simple
                obj = db.session.query(self.model_class).get(identifier)

            if not obj:
                return False

            db.session.delete(obj)
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Erreur lors de la suppression: {str(e)}")

    def get_paginated(self, page: int = 1, per_page: int = 5) -> Tuple[List[Any], int]:
        """Récupère les enregistrements paginés."""
        return self._execute_query(
            query=db.session.query(self.model_class),
            page=page,
            per_page=per_page
        )

    def get_with_filters(self, filters: dict, page: int = 1, per_page: int = 5) -> Tuple[List[Any], int]:
        """Récupère avec filtres avancés et pagination."""
        query = self._apply_filters(
            query=db.session.query(self.model_class),
            filters=filters
        )
        return self._execute_query(query, page, per_page)

    def get_with_filters_and_sort(self, filters: dict, sort_params: list,
                                  page: int = 1, per_page: int = 5) -> Tuple[List[Any], int]:
        """Récupère avec filtres avancés, tri et pagination."""
        query = self._apply_filters(
            query=db.session.query(self.model_class),
            filters=filters
        )
        query = self._apply_sorting(query, sort_params)
        return self._execute_query(query, page, per_page)

    def get_table_schema(self) -> Dict[str, Dict[str, Any]]:
        """Retourne le schéma complet de la table avec les clés primaires correctes."""
        try:
            inspector = inspect(db.engine)
            columns = inspector.get_columns(self.table_name)
            primary_keys = {col.name for col in self.model_class.__table__.primary_key}

            schema = {}
            for col_info in columns:
                col_name = col_info['name']
                schema[col_name] = {
                    'type': str(col_info['type']),
                    'nullable': col_info['nullable'],
                    'primary_key': col_name in primary_keys,  # Correction ici
                    'default': col_info.get('default'),
                    'autoincrement': col_info.get('autoincrement', False)
                }
            return schema
        except Exception as e:
            raise Exception(f"Erreur récupération schéma: {str(e)}")

    def get_table_structure(self) -> Dict[str, List[str]]:
        """Retourne la structure de la table (noms des colonnes)."""
        try:
            inspector = inspect(db.engine)
            return {
                self.table_name: [
                    col['name'] for col in inspector.get_columns(self.table_name)
                ]
            }
        except Exception as e:
            raise Exception(f"Erreur récupération structure: {str(e)}")

    def get_column_schema(self, column_name: str) -> Dict[str, Any]:
        """Récupère le schéma d'une colonne spécifique avec gestion des ENUM."""
        try:
            column = getattr(self.model_class, column_name, None)
            if column is None:
                return {"error": f"Colonne {column_name} non trouvée"}

            if not hasattr(column, 'type'):
                return {"error": "Type de colonne indéterminé"}

            schema = {
                "name": column_name,
                "type": str(column.type),
                "nullable": column.nullable
            }

            if hasattr(column.type, 'enums'):
                schema.update({
                    "type": "ENUM",
                    "values": column.type.enums
                })

            return schema
        except Exception as e:
            return {"error": str(e)}

    def get_enum_values(self, column_name: str) -> Optional[List[str]]:
        """Récupère les valeurs possibles pour une colonne ENUM."""
        try:
            column = self.model_class.__table__.columns.get(column_name)
            return column.type.enums if column and hasattr(column.type, 'enums') else None
        except Exception as e:
            raise Exception(f"Erreur récupération valeurs ENUM: {str(e)}")

    def get_primary_key(self, item) -> str:
        """Récupère le nom de la colonne clé primaire."""
        mapper = class_mapper(self.model_class)
        if not mapper.primary_key:
            raise ValueError("Aucune clé primaire définie pour ce modèle")
        return mapper.primary_key[0].name

    def _validate_data(self, data: Dict[str, Any]) -> None:
        """Valide les données selon les contraintes de la table."""
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

    def _validate_with_schema(self, data: Dict[str, Any]) -> None:
        """Valide les données selon un schéma de validation optionnel."""
        schema = getattr(self.model_class, 'validation_schema')
        errors = {}

        for field, rules in schema.items():
            if field not in data:
                continue

            value = data[field]
            if 'type' in rules and not isinstance(value, eval(rules['type'])):
                errors[field] = f"Doit être de type {rules['type']}"

            if 'maxlength' in rules and len(str(value)) > rules['maxlength']:
                errors[field] = f"Ne doit pas dépasser {rules['maxlength']} caractères"

            if 'regex' in rules and not re.match(rules['regex'], str(value)):
                errors[field] = "Format invalide"

        if errors:
            raise ValueError(json.dumps({"errors": errors}))

    def _apply_filters(self, query, filters: dict):
        """Applique les filtres à une requête."""
        for filter_key, value in filters.items():
            if "__" in filter_key:
                column, operator = filter_key.split("__")
            else:
                column = filter_key
                operator = "eq"

            column_attr = getattr(self.model_class, column, None)
            if column_attr is None:
                continue

            if operator in self.FILTER_OPERATORS:
                query = query.filter(self.FILTER_OPERATORS[operator](column_attr, value))

        return query

    def _apply_sorting(self, query, sort_params: list):
        """Applique le tri à une requête."""
        for column, direction in sort_params:
            column_attr = getattr(self.model_class, column, None)
            if column_attr is not None:
                query = query.order_by(desc(column_attr) if direction == 'desc' else asc(column_attr))
        return query

    def _execute_query(self, query, page: int, per_page: int) -> Tuple[List[Any], int]:
        """Exécute une requête avec pagination."""
        try:
            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
        except SQLAlchemyError as e:
            raise self._handle_db_error("requêtage", e)

    def get_with_filters_and_sort_no_pagination(self, filters: dict, sort_params: list) -> List[Any]:
        """Récupère les données avec filtres et tri sans pagination (pour export)"""
        query = self._apply_filters(
            query=db.session.query(self.model_class),
            filters=filters
        )
        query = self._apply_sorting(query, sort_params)

        try:
            return query.all()
        except SQLAlchemyError as e:
            raise self._handle_db_error("requêtage sans pagination", e)

    def _handle_db_error(self, operation: str, error: Exception) -> Exception:
        """Gère les erreurs de base de données."""
        return Exception(f"Erreur lors de la {operation}: {str(error)}")

    def _handle_validation_error(self, error: ValueError) -> ValueError:
        """Gère les erreurs de validation."""
        try:
            error_data = json.loads(str(error))
            return ValueError(json.dumps(error_data))
        except json.JSONDecodeError:
            return ValueError(json.dumps({"errors": {"general": str(error)}}))
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

