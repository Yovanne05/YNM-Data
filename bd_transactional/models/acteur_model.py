from bd_transactional.models.generic_model import GenericModel
from databases.db import db


class Acteur(GenericModel):
    __tablename__ = 'Acteur'

    idActeur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    dateNaissance = db.Column(db.Date, nullable=False)
    dateDeces = db.Column(db.Date)