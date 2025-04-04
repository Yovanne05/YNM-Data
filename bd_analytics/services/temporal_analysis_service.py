from datetime import datetime
import pandas as pd
from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_session

def analyze_views_over_time(period='month'):
    """
    Analyse des visionnages dans le temps avec le nom des séries/films.

    Args:
        period (str): Niveau d'agrégation ('day', 'month' ou 'year'). Défaut: 'month'

    Returns:
        pd.DataFrame: Colonnes:
            - period: Période temporelle
            - title: Nom du contenu
            - view_count: Nombre de visionnages

    Raises:
        Exception: Erreurs de base de données
    """
    with get_db_session() as session:
        try:
            if period == 'month':
                time_col = func.concat(
                    db.models.TempsDim.annee, '-',
                    func.lpad(db.models.TempsDim.mois, 2, '0')
                )
            elif period == 'year':
                time_col = func.cast(db.models.TempsDim.annee, db.String)
            else:
                time_col = func.concat(
                    db.models.TempsDim.annee, '-',
                    func.lpad(db.models.TempsDim.mois, 2, '0'), '-',
                    func.lpad(db.models.TempsDim.jour, 2, '0')
                )

            query = session.query(
                time_col.label('period'),
                db.models.TitreDim.nom.label('title'),
                func.count(db.models.VisionnageFact.idVisionnage).label('view_count')
            ).join(
                db.models.TempsDim,
                db.models.VisionnageFact.idDate == db.models.TempsDim.idDate
            ).join(
                db.models.TitreDim,
                db.models.VisionnageFact.idTitre == db.models.TitreDim.idTitre
            ).group_by(
                time_col, db.models.TitreDim.nom
            ).order_by(
                time_col, db.models.TitreDim.nom
            )

            return pd.read_sql(query.statement, session.bind)

        except Exception as e:
            raise Exception(f"Database error: {str(e)}")