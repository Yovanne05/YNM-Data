from models.transactional.generic_model import GenericModel
from databases.db import db


class Titre(GenericModel):
    __tablename__ = 'titre'

    idTitre = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    dateDebutLicence = db.Column(db.Date, nullable=False)
    dateFinLicence = db.Column(db.Date, nullable=False)
    categorieAge = db.Column(db.Enum('Tout public', '12+', '16+', '18+'), nullable=False)
    description = db.Column(db.Text)

    film = db.relationship('Film', backref='titre', uselist=False)
    serie = db.relationship('Serie', backref='titre', uselist=False)