from bd_transactional.models.generic_model import GenericModel
from databases.db import db


class Titre(GenericModel):
    __tablename__ = 'Titre'

    idTitre = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    dateDebutLicence = db.Column(db.Date, nullable=False)
    dateFinLicence = db.Column(db.Date, nullable=False)
    categorieAge = db.Column(db.Enum('Tout public', '12+', '16+', '18+'), nullable=False)
    description = db.Column(db.Text)

    film = db.relationship('Film', cascade='all,delete', backref='titres', uselist=False)
    serie = db.relationship('Serie', cascade='all,delete', backref='titres', uselist=False)
    titre_genre = db.relationship('TitreGenre', cascade='all,delete', backref='titres')
    languedisponible = db.relationship('LangueDisponible', cascade='all,delete', backref='titres')
    acting = db.relationship('Acting', cascade='all,delete', backref='titres')
    maliste = db.relationship('MaListe', cascade='all,delete', backref='titres')
    evaluation = db.relationship('Evaluation', cascade='all,delete', backref='titres')