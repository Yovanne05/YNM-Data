from sqlalchemy import func, case, and_, distinct
from sqlalchemy.orm import sessionmaker

from ..models.dimensions.utilisateur_model import UtilisateurDim
from ..models.dimensions.temps_model import TempsDim
from ..models.dimensions.titre_model import TitreDim
from ..models.dimensions.genre_model import GenreDim
from ..models.facts.visionnage_model import VisionnageFact
import pandas as pd
from databases.db import db
from sqlalchemy.exc import SQLAlchemyError


class BehaviorAnalysisService:
    def __init__(self):

        engine = db.get_engine(bind='entrepot')
        session = sessionmaker(bind=engine)
        self.session = session()

        if not hasattr(self.session, 'bind') or self.session.bind is None:
            raise RuntimeError("La session n'a pas de connexion à la base de données configurée")

    def get_viewing_behavior(self, time_dimension='month', user_segment=None, content_filter=None):
        """
        Analyse approfondie du comportement de visionnage
        """
        try:
            # 1. Vérification de la connexion
            if not self.session.is_active:
                self.session = db.session

            time_columns = {
                'day': [TempsDim.jour, TempsDim.mois, TempsDim.annee],
                'month': [TempsDim.mois, TempsDim.annee],
                'quarter': [TempsDim.trimestre, TempsDim.annee],
                'year': [TempsDim.annee]
            }

            if time_dimension not in time_columns:
                raise ValueError(f"Dimension temporelle invalide: {time_dimension}")

            select_columns = [
                *time_columns[time_dimension],
                func.count(VisionnageFact.idVisionnage).label('view_count'),
                func.sum(VisionnageFact.dureeVisionnage).label('total_watch_time'),
                func.count(distinct(VisionnageFact.idUtilisateur)).label('unique_users')
            ]

            if user_segment == 'age_group':
                select_columns.append(
                    case(
                        [
                            (UtilisateurDim.age < 18, 'Jeune'),
                            (UtilisateurDim.age < 35, 'Adulte'),
                            (UtilisateurDim.age >= 35, 'Senior')
                        ],
                        else_='Non spécifié'
                    ).label('age_group')
                )
            elif user_segment == 'country':
                select_columns.append(UtilisateurDim.paysResidence.label('country'))
            elif user_segment == 'subscription_type':
                select_columns.append(UtilisateurDim.typeAbonnement.label('subscription_type'))

            query = self.session.query(*select_columns)

            query = query.join(UtilisateurDim, VisionnageFact.idUtilisateur == UtilisateurDim.idUtilisateur)
            query = query.join(TempsDim, VisionnageFact.idDate == TempsDim.idDate)
            query = query.join(TitreDim, VisionnageFact.idTitre == TitreDim.idTitre)

            if content_filter:
                if content_filter.get('content_type'):
                    query = query.filter(TitreDim.typeTitre == content_filter['content_type'])
                if content_filter.get('genres'):
                    query = query.join(GenreDim, VisionnageFact.idGenre == GenreDim.idGenre)
                    query = query.filter(GenreDim.nomGenre.in_(content_filter['genres']))
                if content_filter.get('date_range'):
                    date_debut, date_fin = content_filter['date_range']
                    query = query.filter(and_(
                        TempsDim.date >= date_debut,
                        TempsDim.date <= date_fin
                    ))

            group_by = time_columns[time_dimension].copy()
            if user_segment:
                group_by.append(user_segment)

            query = query.group_by(*group_by)

            with self.session.connection() as connection:
                df = pd.read_sql(
                    query.statement,
                    connection,
                    params=query.statement.compile().params
                )

            return df

        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Erreur de base de données: {str(e)}")
        except Exception as e:
            raise Exception(f"Erreur inattendue: {str(e)}")
        finally:
            self.session.close()

    def analyze_engagement_metrics(self, user_id=None):
        try:
            if not self.session.is_active:
                self.session = db.session

            query = self.session.query(
                func.avg(VisionnageFact.dureeVisionnage).label('avg_session_duration'),
                func.count(VisionnageFact.idVisionnage).label('total_sessions'),
                func.count(distinct(VisionnageFact.idTitre)).label('unique_content_viewed')
            )

            if user_id:
                query = query.filter(VisionnageFact.idUtilisateur == user_id)

            result = query.one()

            return {
                'avg_session_minutes': round(result.avg_session_duration / 60, 2),
                'sessions_per_user': result.total_sessions,
                'content_variety': result.unique_content_viewed
            }

        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Erreur de base de données: {str(e)}")
        except Exception as e:
            raise Exception(f"Erreur inattendue: {str(e)}")
        finally:
            self.session.close()