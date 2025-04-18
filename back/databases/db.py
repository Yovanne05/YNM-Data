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
from bd_analytics.models.serie_model import SerieEntrepot
from bd_analytics.models.film_model import FilmEntrepot

from bd_transactional.models.abonnement_model import Abonnement
from bd_transactional.models.acteur_model import Acteur
from bd_transactional.models.acting_model import Acting
from bd_transactional.models.evaluation_model import Evaluation
from bd_transactional.models.film_model import Film
from bd_transactional.models.genre_model import Genre
from bd_transactional.models.langue_model import Langue
from bd_transactional.models.languedispo_model import LangueDisponible
from bd_transactional.models.maliste_model import MaListe
from bd_transactional.models.paiement_model import Paiement
from bd_transactional.models.profil_model import Profil
from bd_transactional.models.realisation_model import Realisation
from bd_transactional.models.serie_model import Serie
from bd_transactional.models.studio_model import Studio
from bd_transactional.models.titre_model import Titre
from bd_transactional.models.titregenre_model import TitreGenre
from bd_transactional.models.utilisateur_model import Utilisateur

from bd_analytics.models.facts.evaluation_model import EvaluationFact
from bd_analytics.models.facts.paiement_model import PaiementFact
from bd_analytics.models.facts.visionnage_model import VisionnageFact

db.models = ModelRegistry(db)

db.models.register('Abonnement', Abonnement)
db.models.register('Acteur', Acteur)
db.models.register('Acting', Acting)
db.models.register('Evaluation', Evaluation)
db.models.register('Film', Film)
db.models.register('Genre', Genre)
db.models.register('Langue', Langue)
db.models.register('LangueDisponible', LangueDisponible)
db.models.register('MaListe', MaListe)
db.models.register('Paiement', Paiement)
db.models.register('Profil', Profil)
db.models.register('Realisation', Realisation)
db.models.register('Studio', Studio)
db.models.register('Serie', Serie)
db.models.register('Titre', Titre)
db.models.register('TitreGenre', TitreGenre)
db.models.register('Utilisateur', Utilisateur)

db.models.register('AbonnementDim', AbonnementDim)
db.models.register('GenreDim', GenreDim)
db.models.register('LangueDim', LangueDim)
db.models.register('LangueDisponibleDim', LangueDisponibleDim)
db.models.register('TempsDim', TempsDim)
db.models.register('TitreDim', TitreDim)
db.models.register('UtilisateurDim', UtilisateurDim)
db.models.register('SerieDim', SerieEntrepot)
db.models.register('FilmDim', FilmEntrepot)
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