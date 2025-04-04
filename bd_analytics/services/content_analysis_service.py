import pandas as pd
from sqlalchemy import func
from databases.db import db
from databases.database_session import get_db_session

def get_content_performance(time_range=None):
    """
    Analyse la performance des contenus (films/séries) selon différents critères.

    Args:
        time_range (tuple): Plage optionnelle (start_date, end_date)

    Returns:
        pd.DataFrame: DataFrame contenant:
            - content_title: Titre du contenu
            - content_type: Type de contenu (Film/Série)
            - view_count: Nombre de visionnages
    """
    with get_db_session() as session:
        TitreDim = db.models.TitreDim
        VisionnageFact = db.models.VisionnageFact

        query = session.query(
            TitreDim.nom.label('content_title'),
            TitreDim.typeTitre.label('content_type'),
            func.count(VisionnageFact.idVisionnage).label('view_count')
        ).join(VisionnageFact)

        if time_range:
            query = query.join(db.models.TempsDim).filter(
                db.models.TempsDim.date >= time_range[0],
                db.models.TempsDim.date <= time_range[1]
            )

        query = query.group_by(TitreDim.idTitre, TitreDim.nom, TitreDim.typeTitre)
        return pd.read_sql(query.statement, session.bind)

def get_top_content(top_n=10):
    """
    Récupère les contenus les plus populaires selon le nombre de visionnages.

    Args:
        top_n (int): Nombre de contenus à retourner (10 par défaut)

    Returns:
        pd.DataFrame: DataFrame contenant:
            - content_title: Titre du contenu
            - view_count: Nombre de visionnages
    """
    with get_db_session() as session:
        TitreDim = db.models.TitreDim
        VisionnageFact = db.models.VisionnageFact

        query = session.query(
            TitreDim.nom.label('content_title'),
            func.count(VisionnageFact.idVisionnage).label('view_count')
        ).join(VisionnageFact
               ).group_by(TitreDim.idTitre
                          ).order_by(func.count(VisionnageFact.idVisionnage).desc()
                                     ).limit(top_n)

        return pd.read_sql(query.statement, session.bind)