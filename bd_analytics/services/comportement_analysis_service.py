from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_entrepot_session
from ..services.olap_service import OLAPService


def get_viewing_analytics():
    """
    Mesure l'activité de visionnage en utilisant OLAPService

    Returns:
        dict: {
            'total_views': (int) nombre total de visionnages,
            'avg_duration_minutes': (float) durée moyenne en minutes,
            'users': [
                {
                    'user_id': int,
                    'total_views': int,
                    'avg_duration_minutes': float
                },
                ...
            ]
        }
    """
    with get_db_entrepot_session() as session:
        try:
            olap = OLAPService(session)
            global_stats = {
                'total_views': 0,
                'avg_duration_minutes': 0,
                'users': []
            }

            # Stats globales (totaux)
            result = olap.scoping(
                fact_table=db.models.VisionnageFact,
                dimensions=[],
                measures=['idVisionnage', 'dureeVisionnage'],
                aggregation_funcs={
                    'idVisionnage': func.count,
                    'dureeVisionnage': func.avg
                }
            )

            if not result.empty:
                global_stats['total_views'] = int(result.iloc[0]['aggregated_idVisionnage'])
                duree_moyenne = result.iloc[0]['aggregated_dureeVisionnage']
                global_stats['avg_duration_minutes'] = round((duree_moyenne or 0) / 60, 2)

                # Stats par utilisateur
                user_stats = olap.scoping(
                    fact_table=db.models.VisionnageFact,
                    dimensions=[db.models.VisionnageFact.idUtilisateur],
                    measures=['idVisionnage', 'dureeVisionnage'],
                    aggregation_funcs={
                        'idVisionnage': func.count,
                        'dureeVisionnage': func.avg
                    }
                )

                if not user_stats.empty:
                    global_stats['users'] = [
                        {
                            'user_id': int(row['idUtilisateur']),
                            'total_views': int(row['aggregated_idVisionnage']),
                            'avg_duration_minutes': round((row['aggregated_dureeVisionnage'] or 0) / 60, 2)
                        }
                        for _, row in user_stats.iterrows()
                    ]

            return global_stats

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
    with get_db_entrepot_session() as session:
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
                aggregation_funcs={'idVisionnage': func.count},
                joins=[db.models.TempsDim]
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