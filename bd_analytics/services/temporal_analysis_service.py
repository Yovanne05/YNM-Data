from datetime import datetime
from operator import and_

import pandas as pd
from sqlalchemy import between, func
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import between

from ..models.dimensions.temps_model import TempsDim
from ..models.facts.visionnage_model import VisionnageFact
from ..models.facts.paiement_model import PaiementFact
from databases.db import db


class TemporalAnalysisService:
    def __init__(self):
        engine = db.get_engine(bind='entrepot')
        session = sessionmaker(bind=engine)
        self.session = session()

    def get_time_series_analysis(self, metric='views', period='monthly', last_n=12):
        """
        Analyse des séries temporelles pour différents indicateurs
        Args:
            metric: 'views', 'revenue', 'new_users'
            period: 'daily', 'weekly', 'monthly', 'quarterly'
            last_n: nombre de périodes à analyser
        Returns:
            DataFrame avec l'évolution temporelle
        """
        end_date = datetime.now()

        if period == 'monthly':
            start_date = end_date - relativedelta(months=last_n)
            time_col = func.date_format(TempsDim.idDate, '%Y-%m')
        elif period == 'quarterly':
            start_date = end_date - relativedelta(months=last_n * 3)
            time_col = func.concat(TempsDim.annee, '-Q', TempsDim.trimestre)

        # Sélection de la métrique
        if metric == 'views':
            base_query = self.session.query(
                func.count(VisionnageFact.idVisionnage)
            ).join(TempsDim)
        elif metric == 'revenue':
            base_query = self.session.query(
                func.sum(PaiementFact.montant)
            ).join(TempsDim)

        query = base_query.add_column(
            time_col.label('period')
        ).filter(
            between(TempsDim.idDate, start_date, end_date)
        ).group_by('period').order_by('period')

        df = pd.read_sql(query.statement, self.session.bind)
        df = df.rename(columns={df.columns[0]: metric})

        # Calcul des variations
        df['change'] = df[metric].pct_change() * 100
        df['rolling_avg'] = df[metric].rolling(window=3).mean()

        return df

    def get_period_metrics(self, start_date, end_date):
        """
        Récupère les métriques pour une période donnée
        Args:
            start_date: Date de début
            end_date: Date de fin
        Returns:
            Dictionnaire des métriques pour la période
        """
        try:
            result = self.session.query(
                func.coalesce(func.count(VisionnageFact.idVisionnage), 0).label('views'),
                func.coalesce(func.sum(VisionnageFact.dureeVisionnage), 0).label('watch_time'),
                func.coalesce(func.sum(PaiementFact.montant), 0).label('revenue')
            ).join(
                TempsDim, VisionnageFact.idDate == TempsDim.idDate
            ).filter(
                TempsDim.idDate >= start_date,
                TempsDim.idDate <= end_date
            ).one()

            return {'views': result.views, 'watch_time': result.watch_time, 'revenue': result.revenue}

        except Exception as e:
            self.session.rollback()
            return {'views': 0, 'watch_time': 0, 'revenue': 0}

    def compare_periods(self, metric, period1, period2):
        """
        Comparaison détaillée entre deux périodes
        Args:
            metric: 'views', 'watch_time', 'revenue'
            period1/period2: tuples (start_date, end_date)
        Returns:
            Dict avec comparaison complète
        """
        try:
            p1 = self.get_period_metrics(*period1)
            p2 = self.get_period_metrics(*period2)

            for k in p1:
                p1[k] = p1[k] or 0
                p2[k] = p2[k] or 0

            comparison = {
                'absolute_diff': {k: p2[k] - p1[k] for k in p1},
                'percentage_change': {
                    k: ((p2[k] - p1[k]) / p1[k] * 100) if p1[k] != 0 else (float('inf') if p2[k] > 0 else 0)
                    for k in p1
                },
                'period1': p1,
                'period2': p2,
                'comparison_metric': metric
            }

            return comparison

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Erreur lors de la comparaison des périodes: {str(e)}")