from sqlalchemy import func, distinct
import pandas as pd
from ..utils.filters import ContentFilters
from ..utils.olap_query_builder import OLAPQueryBuilder
from ..utils.time_utils import TimeDimensionHelper
from databases.db import db

class ComportementAnalysisService:
    def __init__(self):
        engine = db.get_engine(bind='entrepot')
        Session = db.sessionmaker(bind=engine)
        self.session = Session()
        self.query_builder = OLAPQueryBuilder(self.session)
        self.filters = ContentFilters()

    def get_viewing_behavior(self, time_dimension='month', content_filter=None):
        try:
            TempsDim = db.models.TempsDim
            VisionnageFact = db.models.VisionnageFact

            # Construction de la requête
            time_cols = TimeDimensionHelper.get_time_columns(time_dimension)
            time_attributes = [getattr(TempsDim, col) for col in time_cols]

            query = self.session.query(
                *time_attributes,
                func.count(VisionnageFact.idVisionnage).label('view_count'),
                func.sum(VisionnageFact.dureeVisionnage).label('total_watch_time'),
                func.count(distinct(VisionnageFact.idUtilisateur)).label('unique_users')
            ).join(
                TempsDim,
                VisionnageFact.idDate == TempsDim.idDate
            )

            if content_filter:
                query = self.filters.apply_content_filters(query, content_filter)

            query = query.group_by(*time_attributes)
            return pd.read_sql(query.statement, self.session.bind)

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Erreur de base de données : {str(e)}")
        finally:
            self.session.close()

    def analyze_engagement_metrics(self, user_id=None):
        try:
            VisionnageFact = db.models.VisionnageFact

            query = self.session.query(
                func.avg(VisionnageFact.dureeVisionnage).label('avg_duration'),
                func.count(VisionnageFact.idVisionnage).label('total_sessions'),
                func.count(distinct(VisionnageFact.idTitre)).label('unique_content')
            )

            if user_id:
                query = query.filter(VisionnageFact.idUtilisateur == user_id)

            result = query.one()
            return {
                'avg_session_minutes': round((result.avg_duration or 0) / 60, 2),
                'sessions_per_user': result.total_sessions or 0,
                'content_variety': result.unique_content or 0
            }

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Erreur de base de données : {str(e)}")
        finally:
            self.session.close()