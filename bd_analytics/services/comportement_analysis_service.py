from sqlalchemy import func
import pandas as pd
from databases.db import db
from databases.database_session import get_db_session

def get_viewing_analytics(user_id=None):
    """
    Mesure l'activité de visionnage d'un utilisateur ou de l'ensemble des utilisateurs

    Args:
        user_id (int, optional): ID utilisateur spécifique. None pour une analyse globale.

    Returns:
        dict: {
            'total_views': (int) nombre total de contenus visionnés,
            'avg_duration_minutes': (float) durée moyenne en minutes
        }
    """
    with get_db_session() as session:
        try:
            VisionnageFact = db.models.VisionnageFact

            query = session.query(
                func.count(VisionnageFact.idVisionnage).label('total_views'),
                func.avg(VisionnageFact.dureeVisionnage).label('avg_duration')
            )

            if user_id:
                query = query.filter(VisionnageFact.idUtilisateur == user_id)

            result = query.one()

            return {
                'total_views': result.total_views,
                'avg_duration_minutes': round(result.avg_duration / 60, 2) if result.avg_duration else 0
            }

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")

def get_daily_viewing_activity():
    """
    Analyse les habitudes de visionnage par date en utilisant les champs disponibles (année, mois, jour).

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
            TempsDim = db.models.TempsDim
            VisionnageFact = db.models.VisionnageFact

            query_date = session.query(
                func.concat(
                    TempsDim.annee, '-',
                    func.lpad(TempsDim.mois, 2, '0'), '-',
                    func.lpad(TempsDim.jour, 2, '0')
                ).label('date'),
                func.count(VisionnageFact.idVisionnage).label('view_count')
            ).join(VisionnageFact
            ).group_by(TempsDim.annee, TempsDim.mois, TempsDim.jour)

            return {
                'by_date': pd.read_sql(query_date.statement, session.bind).to_dict('records')
            }

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")