from operator import and_

import pandas as pd
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

from ..models.dimensions.temps_model import TempsDim
from ..models.dimensions.titre_model import TitreDim
from ..models.dimensions.genre_model import GenreDim
from ..models.facts.visionnage_model import VisionnageFact
from ..models.facts.evaluation_model import EvaluationFact
from databases.db import db


class ContentAnalysisService:
    def __init__(self):

        engine = db.get_engine(bind='entrepot')
        session = sessionmaker(bind=engine)
        self.session = session()

    def get_content_performance(self, performance_metric='views', time_range=None):
        """
        Analyse la performance des contenus selon différents critères
        Args:
            performance_metric: 'views', 'watch_time', 'rating'
            time_range: (start_date, end_date)
        Returns:
            DataFrame avec classement des contenus
        """
        metrics = {
            'views': func.count(VisionnageFact.idVisionnage),
            'watch_time': func.sum(VisionnageFact.dureeVisionnage),
            'rating': func.avg(EvaluationFact.note)
        }

        query = self.session.query(
            TitreDim.nom.label('content_title'),
            TitreDim.typeTitre.label('content_type'),
            metrics[performance_metric].label('metric_value')
        )

        if performance_metric == 'rating':
            query = query.join(EvaluationFact)
        else:
            query = query.join(VisionnageFact)

        if time_range:
            query = query.join(TempsDim).filter(
                and_(
                    TempsDim.annee >= time_range[0].year,
                    TempsDim.annee <= time_range[1].year
                )
            )

        query = query.group_by(TitreDim.idTitre, TitreDim.nom, TitreDim.typeTitre)
        query = query.order_by(desc('metric_value')).limit(100)

        return pd.read_sql(query.statement, self.session.bind)

    def analyze_genre_performance(self):
        """Analyse comparative des performances par genre"""
        query = self.session.query(
            GenreDim.nomGenre.label('genre'),
            func.count(VisionnageFact.idVisionnage).label('view_count'),
            func.avg(EvaluationFact.note).label('avg_rating'),
            func.sum(VisionnageFact.dureeVisionnage).label('total_watch_time')
        )

        query = query.join(
            VisionnageFact,
            VisionnageFact.idGenre == GenreDim.idGenre
        ).join(
            EvaluationFact,
            EvaluationFact.idTitre == VisionnageFact.idTitre
        )

        query = query.group_by(GenreDim.nomGenre)
        query = query.order_by(desc('view_count'))

        df = pd.read_sql(query.statement, self.session.bind)

        df['watch_time_per_view'] = df['total_watch_time'] / df['view_count']
        return df