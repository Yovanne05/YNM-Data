from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_entrepot_session
from ..services.olap_service import OLAPService


def analyze_views_over_time(period='month'):
    with get_db_entrepot_session() as session:
        try:
            olap = OLAPService(session)

            dimensions = []
            if period == 'year':
                dimensions = [db.models.TempsDim.annee]
            elif period == 'month':
                dimensions = [db.models.TempsDim.annee, db.models.TempsDim.mois]
            else:  # day
                dimensions = [db.models.TempsDim.annee, db.models.TempsDim.mois, db.models.TempsDim.jour]

            dimensions.append(db.models.TitreDim.nom)

            result = olap.scoping(
                fact_table=db.models.VisionnageFact,
                dimensions=dimensions,
                measures=['dureeVisionnage'],
                aggregation_funcs={'dureeVisionnage': func.sum}
            )

            result = result.rename(columns={
                'annee': 'year',
                'mois': 'month',
                'jour': 'day',
                'nom': 'title',
                'aggregated_dureeVisionnage': 'total_duration'
            })

            result['view_count'] = 1

            if period == 'day':
                result['period'] = (result['year'].astype(str) + '-' +
                                    result['month'].astype(str).str.zfill(2) + '-' +
                                    result['day'].astype(str).str.zfill(2))
            elif period == 'month':
                result['period'] = (result['year'].astype(str) + '-' +
                                    result['month'].astype(str).str.zfill(2))
            else:
                result['period'] = result['year'].astype(str)

            final_result = result.groupby(['period', 'title']).agg({
                'view_count': 'sum',
                'total_duration': 'sum'
            }).reset_index()

            return final_result.sort_values(['period', 'title'])

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")