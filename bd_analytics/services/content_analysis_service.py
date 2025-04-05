from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_session
from ..services.olap_service import OLAPService


def get_content_performance(time_range=None, time_granularity='month'):
    """
    Analyse la performance des contenus avec granularité temporelle configurable

    Args:
        time_range (tuple): Optionnel (start_date, end_date)
        time_granularity (str): 'day', 'month', 'quarter' ou 'year'

    Returns:
        pd.DataFrame avec colonnes:
            - period: Période temporelle selon la granularité
            - content_title: Titre du contenu
            - content_type: Type de contenu
            - view_count: Nombre de visionnages
    """
    with get_db_session() as session:
        olap = OLAPService(session)

        time_hierarchy = {
            'year': [db.models.TempsDim.annee],
            'quarter': [db.models.TempsDim.annee, db.models.TempsDim.trimestre],
            'month': [db.models.TempsDim.annee, db.models.TempsDim.mois],
            'day': [db.models.TempsDim.annee, db.models.TempsDim.mois, db.models.TempsDim.jour]
        }

        dimensions = time_hierarchy[time_granularity] + [
            db.models.TitreDim.nom,
            db.models.TitreDim.typeTitre
        ]

        filters = {}
        if time_range:
            filters = {
                'TempsDim.date': f'>= {time_range[0]}',
                'TempsDim.date': f'<= {time_range[1]}'
            }

        result = olap.scoping(
            fact_table=db.models.VisionnageFact,
            dimensions=dimensions,
            measures=['idVisionnage'],
            filters=filters,
            aggregation_funcs={'idVisionnage': func.count}
        )

        result = result.rename(columns={
            'nom': 'content_title',
            'typeTitre': 'content_type',
            'aggregated_idVisionnage': 'view_count'
        })

        if time_granularity == 'day':
            result['period'] = (result['annee'].astype(str) + '-' +
                                result['mois'].astype(str).str.zfill(2) + '-' +
                                result['jour'].astype(str).str.zfill(2))
        elif time_granularity == 'month':
            result['period'] = (result['annee'].astype(str) + '-' +
                                result['mois'].astype(str).str.zfill(2))
        elif time_granularity == 'quarter':
            result['period'] = (result['annee'].astype(str) + 'T' +
                                result['trimestre'].astype(str))
        else:  # year
            result['period'] = result['annee'].astype(str)

        return result[['period', 'content_title', 'content_type', 'view_count']]


def get_top_content(top_n=10, time_range=None, content_type=None):
    """
    Récupère les contenus les plus populaires avec filtres avancés

    Args:
        top_n (int): Nombre de résultats
        time_range (tuple): Filtre temporel optionnel
        content_type (str): 'Film' ou 'Série' pour filtrer

    Returns:
        pd.DataFrame des top contenus
    """
    with get_db_session() as session:
        df = get_content_performance(time_range=time_range)

        if content_type:
            df = df[df['content_type'] == content_type]

        if 'period' in df.columns:
            df = df.groupby(['content_title', 'content_type'])['view_count'].sum().reset_index()

        return df.sort_values('view_count', ascending=False).head(top_n)