from sqlalchemy import func, and_, case, distinct
from sqlalchemy.orm import aliased
from ..models.facts.visionnage_model import VisionnageFact
from ..models.facts.evaluation_model import EvaluationFact
from ..models.facts.paiement_model import PaiementFact
from ..models.dimensions.utilisateur_model import UtilisateurDim
from ..models.dimensions.temps_model import TempsDim

class OLAPQueryBuilder:
    def __init__(self, session):
        self.session = session

    def build_base_query(self, metrics, dimensions):
        """Construit une requête OLAP de base"""
        selects = []

        # Gestion des métriques
        if 'view_count' in metrics:
            selects.append(func.count(VisionnageFact.idVisionnage).label('view_count'))
        if 'watch_time' in metrics:
            selects.append(func.sum(VisionnageFact.dureeVisionnage).label('total_watch_time'))

        # Gestion des dimensions
        if 'time' in dimensions:
            selects.extend([TempsDim.mois, TempsDim.annee])

        return self.session.query(*selects)

    def apply_time_filter(self, query, date_range):
        """Applique un filtre temporel"""
        if date_range:
            date_debut, date_fin = date_range
            return query.filter(and_(
                TempsDim.annee >= date_debut.year,
                TempsDim.annee <= date_fin.year,
                TempsDim.mois >= date_debut.month,
                TempsDim.mois <= date_fin.month
            ))
        return query