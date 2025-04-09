from bd_transactional.models.generic_model import GenericModel
from databases.db import db


class Utilisateur(GenericModel):
    __tablename__ = 'Utilisateur'

    idUtilisateur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    paysResidance = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True, nullable=False)
    numero = db.Column(db.String(15), unique=True, nullable=False)
    statutAbonnement = db.Column(db.Enum('Actif', 'Résilié'), default='Actif')