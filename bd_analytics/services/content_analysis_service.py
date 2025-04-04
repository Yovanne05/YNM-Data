from sqlalchemy import func
import pandas as pd
from ..utils.filters import ContentFilters
from databases.db import db

class ContentAnalysisService:
    def __init__(self):
        engine = db.get_engine(bind='entrepot')
        Session = db.sessionmaker(bind=engine)
        self.session = Session()
        self.filters = ContentFilters()

    def get_content_performance(self, metric='views', time_range=None):
        try:
            TitreDim = db.models.TitreDim
            VisionnageFact = db.models.VisionnageFact
            EvaluationFact = db.models.EvaluationFact

            if metric == 'rating':
                query = self.session.query(
                    TitreDim.nom.label('content_title'),
                    TitreDim.typeTitre.label('content_type'),
                    func.count(EvaluationFact.idEvaluation).label('rating_count'),
                    func.avg(EvaluationFact.note).label('avg_rating')
                ).join(EvaluationFact)
            else:
                query = self.session.query(
                    TitreDim.nom.label('content_title'),
                    TitreDim.typeTitre.label('content_type'),
                    func.count(VisionnageFact.idVisionnage).label('view_count'),
                    func.sum(VisionnageFact.dureeVisionnage).label('total_watch_time')
                ).join(VisionnageFact)

            if time_range:
                query = self.filters.apply_time_filter(query, {
                    'date_range': time_range
                })

            query = query.group_by(
                TitreDim.idTitre,
                TitreDim.nom,
                TitreDim.typeTitre
            )

            return pd.read_sql(query.statement, self.session.bind)

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            self.session.close()

    def analyze_genre_performance(self):
        try:
            GenreDim = db.models.GenreDim
            VisionnageFact = db.models.VisionnageFact
            EvaluationFact = db.models.EvaluationFact

            query = self.session.query(
                GenreDim.nomGenre.label('genre'),
                func.count(VisionnageFact.idVisionnage).label('view_count'),
                func.sum(VisionnageFact.dureeVisionnage).label('total_watch_time'),
                func.avg(EvaluationFact.note).label('avg_rating')
            ).join(
                VisionnageFact
            ).join(
                EvaluationFact
            ).group_by(
                GenreDim.nomGenre
            )

            df = pd.read_sql(query.statement, self.session.bind)
            df['watch_time_per_view'] = df['total_watch_time'] / df['view_count']
            return df

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            self.session.close()