from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, joinedload
from databases.db import db
from flask import current_app
from sqlalchemy import func, and_, text
from sqlalchemy.inspection import inspect

from bd_analytics.models.dimensions.temps_model import TempsDim
from bd_analytics.models.dimensions.genre_model import GenreDim
from bd_analytics.models.dimensions.titre_model import TitreDim
from bd_analytics.models.facts.visionnage_model import VisionnageFact
from bd_analytics.models.facts.evaluation_model import EvaluationFact
from bd_analytics.models.facts.paiement_model import PaiementFact

class CubeService:
    _bind_key = 'entrepot'

    @classmethod
    def _get_session(cls):
        """Crée une session pour la base secondaire"""
        try:
            engine = db.get_engine(current_app, bind=cls._bind_key)
            Session = sessionmaker(bind=engine)
            return Session()
        except Exception as e:
            current_app.logger.error(f"Erreur création session: {str(e)}")
            raise

    @staticmethod
    def get_top_content(limit: int = 10, genre_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Récupère les contenus les plus populaires"""
        try:
            with CubeService._get_session() as session:
                # Construction de la requête de base
                query = session.query(
                    TitreDim.nom.label('titre'),
                    func.count(VisionnageFact.idVisionnage).label('vues'),
                    func.avg(EvaluationFact.note).label('note_moyenne')
                )

                # Jointures
                query = query.join(VisionnageFact, TitreDim.idTitre == VisionnageFact.idTitre, isouter=True)
                query = query.join(EvaluationFact, TitreDim.idTitre == EvaluationFact.idTitre, isouter=True)

                # Filtres
                if genre_id:
                    query = query.filter(TitreDim.idGenre == genre_id)

                # Groupement et tri
                query = query.group_by(TitreDim.idTitre, TitreDim.nom)
                query = query.order_by(func.count(VisionnageFact.idVisionnage).desc())
                query = query.limit(limit)

                # Exécution
                results = query.all()

                # Formatage des résultats
                return [{
                    'titre': row.titre,
                    'vues': row.vues or 0,
                    'note_moyenne': float(row.note_moyenne) if row.note_moyenne is not None else None
                } for row in results]

        except SQLAlchemyError as e:
            current_app.logger.error(f"Erreur get_top_content: {str(e)}", exc_info=True)
            raise Exception(f"Erreur lors de la récupération des tops contenus: {str(e)}")

    @staticmethod
    def get_visionnages_par_periode(debut: str, fin: str) -> List[Dict[str, Any]]:
        """Récupère les visionnages pour une période donnée"""
        try:
            with CubeService._get_session() as session:
                # Conversion des dates en années (simplifié)
                annee_debut = int(debut[:4]) if debut else 2023
                annee_fin = int(fin[:4]) if fin else 2023

                # Construction de la requête
                query = session.query(
                    TempsDim.annee,
                    TempsDim.mois,
                    func.count(VisionnageFact.idVisionnage).label('total_visionnages')
                )

                # Jointures et filtres
                query = query.join(VisionnageFact, VisionnageFact.idDate == TempsDim.idDate)
                query = query.filter(and_(
                    TempsDim.annee >= annee_debut,
                    TempsDim.annee <= annee_fin
                ))

                # Groupement et tri
                query = query.group_by(TempsDim.annee, TempsDim.mois)
                query = query.order_by(TempsDim.annee, TempsDim.mois)

                # Exécution
                results = query.all()

                # Formatage des résultats
                return [{
                    'annee': row.annee,
                    'mois': row.mois,
                    'total_visionnages': row.total_visionnages
                } for row in results]

        except SQLAlchemyError as e:
            current_app.logger.error(f"Erreur get_visionnages_par_periode: {str(e)}", exc_info=True)
            raise Exception(f"Erreur lors de la récupération des visionnages: {str(e)}")

    @staticmethod
    def test_connection() -> bool:
        """Teste la connexion à la base de données"""
        try:
            with CubeService._get_session() as session:
                result = session.execute(text("SELECT 1")).scalar()
                return result == 1
        except Exception as e:
            current_app.logger.error(f"Erreur test_connection: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def get_table_structure(table_name: str) -> Dict[str, Any]:
        """Récupère la structure d'une table"""
        try:
            engine = db.get_engine(current_app, bind=CubeService._bind_key)
            inspector = inspect(engine)

            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    'name': column['name'],
                    'type': str(column['type']),
                    'nullable': column.get('nullable', False),
                    'primary_key': column.get('primary_key', False)
                })

            return {
                'table_name': table_name,
                'columns': columns
            }
        except Exception as e:
            current_app.logger.error(f"Erreur get_table_structure: {str(e)}", exc_info=True)
            raise Exception(f"Erreur lors de la récupération de la structure: {str(e)}")