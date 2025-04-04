from sqlalchemy import and_
from ..models.dimensions.titre_model import TitreDim
from ..models.dimensions.genre_model import GenreDim
from ..models.dimensions.temps_model import TempsDim
from databases.db import db



class ContentFilters:
    @staticmethod
    def apply_content_filters(query, filters):
        """Applique des filtres de contenu à une requête"""
        if not filters:
            return query

        if filters.get('content_type'):
            query = query.filter(TitreDim.typeTitre == filters['content_type'])

        if filters.get('genres'):
            query = query.join(GenreDim).filter(
                GenreDim.nomGenre.in_(filters['genres'])
            )

        if filters.get('date_range'):
            date_debut, date_fin = filters['date_range']
            query = query.filter(and_(
                TempsDim.date >= date_debut,
                TempsDim.date <= date_fin
            ))

        return query

    def apply_time_filter(self, query, date_range):
        if date_range:
            return query.join(db.models.TempsDim).filter(
                db.models.TempsDim.idDate >= date_range[0],
                db.models.TempsDim.idDate <= date_range[1]
            )
        return query