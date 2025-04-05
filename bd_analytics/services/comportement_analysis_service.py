from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_session
from ..services.olap_service import OLAPService


def get_viewing_analytics(user_id=None):
    """
    Mesure l'activité de visionnage en utilisant OLAPService

    Args:
        user_id (int, optional): ID utilisateur spécifique. None pour analyse globale.

    Returns:
        dict: {
            'total_views': (int) nombre total de visionnages,
            'avg_duration_minutes': (float) durée moyenne en minutes
        }
    """
    with get_db_session() as session:
        try:
            olap = OLAPService(session)

            dimensions = []
            measures = ['idVisionnage', 'dureeVisionnage']
            filters = {}

            if user_id:
                filters = {'idUtilisateur': user_id}

            result = olap.scoping(
                fact_table=db.models.VisionnageFact,
                dimensions=dimensions,
                measures=measures,
                filters=filters,
                aggregation_funcs={
                    'idVisionnage': func.count,
                    'dureeVisionnage': func.avg
                }
            )

            if not result.empty:
                return {
                    'total_views': int(result.iloc[0]['aggregated_idVisionnage']),
                    'avg_duration_minutes': round(result.iloc[0]['aggregated_dureeVisionnage'] / 60, 2)
                }
            return {'total_views': 0, 'avg_duration_minutes': 0}

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")


def get_daily_viewing_activity():
    """
    Analyse des habitudes de visionnage par date avec OLAPService

    Returns:
        dict: {
            'by_date': [
                {'date': 'YYYY-MM-DD', 'view_count': int},
                ...
            ]
        }
    """
    with get_db_session() as session:
        try:
            olap = OLAPService(session)

            result = olap.scoping(
                fact_table=db.models.VisionnageFact,
                dimensions=[
                    db.models.TempsDim.annee,
                    db.models.TempsDim.mois,
                    db.models.TempsDim.jour
                ],
                measures=['idVisionnage'],
                aggregation_funcs={'idVisionnage': func.count}
            )

            if not result.empty:
                result['date'] = (
                        result['annee'].astype(str) + '-' +
                        result['mois'].astype(str).str.zfill(2) + '-' +
                        result['jour'].astype(str).str.zfill(2)
                )
                return {
                    'by_date': result[['date', 'aggregated_idVisionnage']]
                    .rename(columns={'aggregated_idVisionnage': 'view_count'})
                    .to_dict('records')
                }
            return {'by_date': []}

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")