import pandas as pd
from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_entrepot_session
from ..services.olap_service import OLAPService


def get_content_performance(time_range=None, time_granularity='month'):
    """
    Analyse la performance des contenus avec granularité temporelle configurable

    Args:
        time_range (tuple): Optionnel (start_date, end_date) au format 'YYYY-MM-DD'
        time_granularity (str): 'day', 'month', 'quarter' ou 'year'

    Returns:
        pd.DataFrame avec colonnes:
            - period: Période temporelle selon la granularité
            - content_title: Titre du contenu
            - content_type: Type de contenu
            - view_count: Nombre total de visionnages
    """
    with get_db_entrepot_session() as session:
        try:
            olap = OLAPService(session)

            time_columns = {
                'year': [db.models.TempsDim.annee],
                'quarter': [db.models.TempsDim.annee, db.models.TempsDim.trimestre],
                'month': [db.models.TempsDim.annee, db.models.TempsDim.mois],
                'day': [db.models.TempsDim.annee, db.models.TempsDim.mois, db.models.TempsDim.jour]
            }[time_granularity]

            dimensions = time_columns + [
                db.models.TitreDim.nom,
                db.models.TitreDim.typeTitre
            ]

            filters = {}
            if time_range:
                start_date, end_date = time_range
                start_parts = list(map(int, start_date.split('-')))
                end_parts = list(map(int, end_date.split('-')))

                if len(start_parts) >= 1:
                    filters['TempsDim.annee'] = start_parts[0]
                if len(start_parts) >= 2:
                    filters['TempsDim.mois'] = start_parts[1]
                if len(start_parts) >= 3:
                    filters['TempsDim.jour'] = start_parts[2]

                if len(end_parts) >= 1:
                    filters['TempsDim.annee'] = end_parts[0]
                if len(end_parts) >= 2:
                    filters['TempsDim.mois'] = end_parts[1]
                if len(end_parts) >= 3:
                    filters['TempsDim.jour'] = end_parts[2]

            joins = [
                (db.models.TempsDim, db.models.VisionnageFact.idDate == db.models.TempsDim.idDate),
                (db.models.TitreDim, db.models.VisionnageFact.idTitre == db.models.TitreDim.idTitre)
            ]

            result = olap.scoping(
                fact_table=db.models.VisionnageFact,
                dimensions=dimensions,
                measures=['nombreVues'],
                filters=filters,
                aggregation_funcs={'nombreVues': func.sum},
                joins=joins
            )

            if result.empty:
                return pd.DataFrame(columns=['period', 'content_title', 'content_type', 'view_count'])

            if time_granularity == 'day':
                result['period'] = (
                    result['annee'].astype(str) + '-' +
                    result['mois'].astype(str).str.zfill(2) + '-' +
                    result['jour'].astype(str).str.zfill(2)
                )
            elif time_granularity == 'month':
                result['period'] = (
                    result['annee'].astype(str) + '-' +
                    result['mois'].astype(str).str.zfill(2)
                )
            elif time_granularity == 'quarter':
                result['period'] = (
                    result['annee'].astype(str) + 'T' +
                    result['trimestre'].astype(str)
                )
            else:  # year
                result['period'] = result['annee'].astype(str)

            return result.rename(columns={
                'nom': 'content_title',
                'typeTitre': 'content_type',
                'aggregated_nombreVues': 'view_count'
            })[['period', 'content_title', 'content_type', 'view_count']]

        except Exception as e:
            raise Exception(f"Database error in get_content_performance: {str(e)}")

def get_top_content(top_n=10, time_range=None, content_type=None):
    """
    Récupère les contenus les plus populaires avec filtres avancés

    Args:
        top_n (int): Nombre de résultats
        time_range (tuple): Filtre temporel optionnel (start_date, end_date)
        content_type (str): 'Film' ou 'Série' pour filtrer

    Returns:
        pd.DataFrame des top contenus avec colonnes:
            - content_title
            - content_type
            - view_count
    """
    try:
        df = get_content_performance(time_range=time_range, time_granularity='day')

        if content_type:
            df = df[df['content_type'] == content_type]

        if 'period' in df.columns:
            df = df.groupby(['content_title', 'content_type'], as_index=False)['view_count'].sum()

        return df.sort_values('view_count', ascending=False).head(top_n)

    except Exception as e:
        raise Exception(f"Error in get_top_content: {str(e)}")