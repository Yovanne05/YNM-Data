from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from databases.db import db
from models.analytics.temps_model import Temps
from flask import current_app
from sqlalchemy import inspect


class TempsService:
    _bind_key = 'entrepot'

    @classmethod
    def _get_session(cls):
        """Crée une session pour la base secondaire"""
        engine = db.get_engine(current_app._get_current_object(), bind=cls._bind_key)
        session = sessionmaker(bind=engine)
        return session()

    @staticmethod
    def get_all() -> List[Temps]:
        """Récupère tous les enregistrements de la table Temps"""
        try:
            with TempsService._get_session() as session:
                return session.query(Temps).all()
        except SQLAlchemyError as e:
            current_app.logger.error(f"Erreur TempsService.get_all: {str(e)}")
            raise Exception(f"Erreur lors de la récupération des données: {str(e)}")

    @staticmethod
    def get_all_as_dict() -> List[Dict[str, Any]]:
        """Récupère tous les enregistrements sous forme de dictionnaire"""
        try:
            with TempsService._get_session() as session:
                temps_list = session.query(Temps).all()
                return [{
                    'idDate': temps.idDate,
                    'jour': temps.jour,
                    'mois': temps.mois,
                    'annee': temps.annee,
                    'trimestre': temps.trimestre
                } for temps in temps_list]
        except SQLAlchemyError as e:
            current_app.logger.error(f"Erreur TempsService.get_all_as_dict: {str(e)}")
            return []

    @staticmethod
    def get_by_id(id_date: int) -> Optional[Temps]:
        """Récupère un enregistrement par son ID"""
        try:
            with TempsService._get_session() as session:
                return session.query(Temps).get(id_date)
        except SQLAlchemyError as e:
            current_app.logger.error(f"Erreur TempsService.get_by_id: {str(e)}")
            raise Exception(f"Erreur lors de la récupération: {str(e)}")

    @staticmethod
    def create(data: Dict[str, Any]) -> Temps:
        """Crée un nouvel enregistrement"""
        try:
            with TempsService._get_session() as session:
                temps = Temps(**data)
                session.add(temps)
                session.commit()
                return temps
        except SQLAlchemyError as e:
            session.rollback()
            current_app.logger.error(f"Erreur TempsService.create: {str(e)}")
            raise Exception(f"Erreur lors de la création: {str(e)}")

    @staticmethod
    def get_table_structure() -> Dict[str, List[str]]:
        """Retourne la structure de la table"""
        try:
            engine = db.get_engine(current_app._get_current_object(), bind=TempsService._bind_key)
            inspector = inspect(engine)
            columns = [col['name'] for col in inspector.get_columns(Temps.__tablename__)]
            return {Temps.__tablename__: columns}
        except Exception as e:
            current_app.logger.error(f"Erreur TempsService.get_table_structure: {str(e)}")
            raise Exception(f"Erreur récupération structure: {str(e)}")