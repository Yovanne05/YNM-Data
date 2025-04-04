from flask_sqlalchemy import SQLAlchemy
from config import config
from databases.model_registry import ModelRegistry

db = SQLAlchemy()

from bd_analytics.models.dimensions.abonnement_model import AbonnementDim
from bd_analytics.models.dimensions.genre_model import GenreDim
from bd_analytics.models.dimensions.langue_model import LangueDim
from bd_analytics.models.dimensions.languedisponible_model import LangueDisponibleDim
from bd_analytics.models.dimensions.temps_model import TempsDim
from bd_analytics.models.dimensions.titre_model import TitreDim
from bd_analytics.models.dimensions.utilisateur_model import UtilisateurDim

from bd_analytics.models.facts.evaluation_model import EvaluationFact
from bd_analytics.models.facts.paiement_model import PaiementFact
from bd_analytics.models.facts.visionnage_model import VisionnageFact

db.models = ModelRegistry()

db.models.register('AbonnementDim', AbonnementDim)
db.models.register('GenreDim', GenreDim)
db.models.register('LangueDim', LangueDim)
db.models.register('LangueDisponibleDim', LangueDisponibleDim)
db.models.register('TempsDim', TempsDim)
db.models.register('TitreDim', TitreDim)
db.models.register('UtilisateurDim', UtilisateurDim)
db.models.register('EvaluationFact', EvaluationFact)
db.models.register('PaiementFact', PaiementFact)
db.models.register('VisionnageFact', VisionnageFact)

def init_app(app):
    """Initialise l'application Flask avec la base de données."""
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    app.config['SQLALCHEMY_BINDS'] = {
        'entrepot': config.entrepot_db_uri
    }

    db.init_app(app)
    with app.app_context():
        db.create_all()