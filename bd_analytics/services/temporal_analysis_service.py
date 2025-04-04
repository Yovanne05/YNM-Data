from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from ..utils.time_utils import TimeDimensionHelper
from databases.db import db


class TemporalAnalysisService:
    def __init__(self):
        engine = db.get_engine(bind='entrepot')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_time_series_analysis(self, metric='views', period='monthly', last_n=12):
        try:
            TempsDim = db.models.TempsDim
            VisionnageFact = db.models.VisionnageFact
            PaiementFact = db.models.PaiementFact

            end_date = datetime.now()
            time_col = TimeDimensionHelper.get_time_column_expression(period)

            if metric == 'views':
                query = self.session.query(
                    func.count(VisionnageFact.idVisionnage).label(metric),
                    time_col.label('period')
                ).join(
                    TempsDim,
                    VisionnageFact.idDate == TempsDim.idDate
                )
            elif metric == 'revenue':
                query = self.session.query(
                    func.sum(PaiementFact.montant).label(metric),
                    time_col.label('period')
                ).join(
                    TempsDim,
                    PaiementFact.idDate == TempsDim.idDate
                )

            start_date = TimeDimensionHelper.calculate_start_date(period, last_n)
            query = query.filter(
                TempsDim.idDate >= start_date,
                TempsDim.idDate <= end_date
            ).group_by('period').order_by('period')

            df = pd.read_sql(query.statement, self.session.bind)

            if not df.empty:
                df['change'] = df[metric].pct_change() * 100
                df['rolling_avg'] = df[metric].rolling(window=3).mean()

            return df

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Erreur lors de l'analyse des séries temporelles: {str(e)}")
        finally:
            self.session.close()

    def compare_periods(self, metric, period1, period2):
        try:
            p1 = self._get_period_metrics(*period1)
            p2 = self._get_period_metrics(*period2)

            comparison = {
                'absolute_diff': {k: p2[k] - p1[k] for k in p1},
                'percentage_change': {
                    k: ((p2[k] - p1[k]) / p1[k] * 100) if p1[k] != 0 else 0
                    for k in p1
                },
                'period1': p1,
                'period2': p2,
                'comparison_metric': metric
            }

            return comparison

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            self.session.close()

    def _get_period_metrics(self, start_date, end_date):
        TempsDim = db.models.TempsDim
        VisionnageFact = db.models.VisionnageFact
        PaiementFact = db.models.PaiementFact

        query = self.session.query(
            func.coalesce(func.count(VisionnageFact.idVisionnage), 0).label('views'),
            func.coalesce(func.sum(VisionnageFact.dureeVisionnage), 0).label('watch_time'),
            func.coalesce(func.sum(PaiementFact.montant), 0).label('revenue')
        ).join(
            TempsDim,
            VisionnageFact.idDate == TempsDim.idDate
        ).filter(
            TempsDim.idDate >= start_date,
            TempsDim.idDate <= end_date
        )

        result = query.one_or_none() or (0, 0, 0)
        return {'views': result[0], 'watch_time': result[1], 'revenue': result[2]}