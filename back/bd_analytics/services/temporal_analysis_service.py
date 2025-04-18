import pandas as pd
from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_entrepot_session
from ..services.olap_service import OLAPService


def analyze_views_over_time(period='year'):
    """
    Analyse l'évolution des visionnages dans le temps en utilisant OLAPService

    Args:
        period (str): 'day', 'month' ou 'year'

    Returns:
        pd.DataFrame avec colonnes:
            - period
            - title
            - view_count
            - total_duration (en secondes)
    """
    with get_db_entrepot_session() as session:
        try:
            olap = OLAPService(session)

            if period == 'year':
                dimensions = [db.models.TempsDim.annee]
            elif period == 'month':
                dimensions = [db.models.TempsDim.annee, db.models.TempsDim.mois]
            else:  # day
                dimensions = [db.models.TempsDim.annee, db.models.TempsDim.mois, db.models.TempsDim.jour]

            dimensions.append(db.models.TitreDim.nom)
            measures = ['nombreVues', 'dureeVisionnage']

            joins = [
                (db.models.TempsDim, db.models.VisionnageFact.idDate == db.models.TempsDim.idDate),
                (db.models.TitreDim, db.models.VisionnageFact.idTitre == db.models.TitreDim.idTitre)
            ]

            result = olap.scoping(
                fact_table=db.models.VisionnageFact,
                dimensions=dimensions,
                measures=measures,
                aggregation_funcs={
                    'nombreVues': func.sum,
                    'dureeVisionnage': func.sum
                },
                joins=joins
            )

            if result.empty:
                return pd.DataFrame(columns=['period', 'title', 'view_count', 'total_duration'])

            result = result.rename(columns={
                'nom': 'title',
                'aggregated_nombreVues': 'view_count',
                'aggregated_dureeVisionnage': 'total_duration'
            })

            if period == 'day':
                result['period'] = (result['annee'].astype(str) + '-' +
                                    result['mois'].astype(str).str.zfill(2) + '-' +
                                    result['jour'].astype(str).str.zfill(2))
            elif period == 'month':
                result['period'] = (result['annee'].astype(str) + '-' +
                                  result['mois'].astype(str).str.zfill(2))
            else:  # year
                result['period'] = result['annee'].astype(str)

            return result[['period', 'title', 'view_count', 'total_duration']].sort_values(['period', 'title'])

        except Exception as e:
            raise Exception(f"Database error in analyze_views_over_time: {str(e)}")