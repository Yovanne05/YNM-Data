from .dimensions.abonnement_model import AbonnementDim
from .facts.evaluation_model import EvaluationFact
from .dimensions.genre_model import GenreDim
from .dimensions.langue_model import LangueDim
from .dimensions.languedisponible_model import LangueDisponibleDim
from .facts.paiement_model import PaiementFact
from .dimensions.temps_model import TempsDim
from .dimensions.titre_model import TitreDim
from .dimensions.utilisateur_model import UtilisateurDim
from .facts.visionnage_model import VisionnageFact
from databases.db import db


def setup_relationships():
    # 1. Relations Utilisateur
    UtilisateurDim._visionnages = db.relationship(
        "VisionnageFact",
        back_populates="utilisateur",
        overlaps="visionnages"
    )

    UtilisateurDim._evaluations = db.relationship(
        "EvaluationFact",
        back_populates="utilisateur",
        overlaps="evaluations"
    )

    UtilisateurDim._paiements = db.relationship(
        "PaiementFact",
        back_populates="utilisateur",
        overlaps="paiements"
    )

    # 2. Relations Visionnage
    VisionnageFact.utilisateur = db.relationship(
        "UtilisateurDim",
        back_populates="_visionnages",
        overlaps="visionnages"
    )

    VisionnageFact.titre = db.relationship(
        "TitreDim",
        back_populates="_visionnages",
        overlaps="titres_visionnages"
    )

    VisionnageFact.temps = db.relationship(
        "TempsDim",
        back_populates="_visionnages",
        overlaps="temps_visionnages"
    )

    VisionnageFact.genre = db.relationship(
        "GenreDim",
        back_populates="_visionnages",
        overlaps="genres_visionnages"
    )

    VisionnageFact.langue_disponible = db.relationship(
        "LangueDisponibleDim",
        back_populates="_visionnages",
        overlaps="langues_visionnages"
    )

    # 3. Relations Evaluation
    EvaluationFact.utilisateur = db.relationship(
        "UtilisateurDim",
        back_populates="_evaluations",
        overlaps="evaluations"
    )

    EvaluationFact.titre = db.relationship(
        "TitreDim",
        back_populates="_evaluations",
        overlaps="titres_evaluations"
    )

    EvaluationFact.genre = db.relationship(
        "GenreDim",
        back_populates="_evaluations",
        overlaps="genres_evaluations"
    )

    EvaluationFact.temps = db.relationship(
        "TempsDim",
        back_populates="_evaluations",
        overlaps="temps_evaluations"
    )

    # 4. Relations Paiement
    PaiementFact.utilisateur = db.relationship(
        "UtilisateurDim",
        back_populates="_paiements",
        overlaps="paiements"
    )

    PaiementFact.abonnement = db.relationship(
        "AbonnementDim",
        back_populates="_paiements",
        overlaps="abonnements_paiements"
    )

    PaiementFact.temps = db.relationship(
        "TempsDim",
        back_populates="_paiements",
        overlaps="temps_paiements"
    )

    # 5. Relations Abonnement
    AbonnementDim._paiements = db.relationship(
        "PaiementFact",
        back_populates="abonnement",
        overlaps="abonnements_paiements"
    )

    # 6. Relations Titre
    TitreDim.genre = db.relationship(
        "GenreDim",
        back_populates="_titres",
        overlaps="genres_titres"
    )

    TitreDim._visionnages = db.relationship(
        "VisionnageFact",
        back_populates="titre",
        overlaps="titres_visionnages"
    )

    TitreDim._evaluations = db.relationship(
        "EvaluationFact",
        back_populates="titre",
        overlaps="titres_evaluations"
    )

    # 7. Relations Genre
    GenreDim._titres = db.relationship(
        "TitreDim",
        back_populates="genre",
        overlaps="genres_titres"
    )

    GenreDim._visionnages = db.relationship(
        "VisionnageFact",
        back_populates="genre",
        overlaps="genres_visionnages"
    )

    GenreDim._evaluations = db.relationship(
        "EvaluationFact",
        back_populates="genre",
        overlaps="genres_evaluations"
    )

    # 8. Relations LangueDisponible
    LangueDisponibleDim._visionnages = db.relationship(
        "VisionnageFact",
        back_populates="langue_disponible",
        overlaps="langues_visionnages"
    )

    LangueDisponibleDim.langue = db.relationship(
        "LangueDim",
        back_populates="_langues_disponibles",
        overlaps="langues_disponibles"
    )

    # 9. Relations Langue
    LangueDim._langues_disponibles = db.relationship(
        "LangueDisponibleDim",
        back_populates="langue",
        overlaps="langues_disponibles"
    )

    # 10. Relations Temps
    TempsDim._visionnages = db.relationship(
        "VisionnageFact",
        back_populates="temps",
        overlaps="temps_visionnages"
    )

    TempsDim._evaluations = db.relationship(
        "EvaluationFact",
        back_populates="temps",
        overlaps="temps_evaluations"
    )

    TempsDim._paiements = db.relationship(
        "PaiementFact",
        back_populates="temps",
        overlaps="temps_paiements"
    )
