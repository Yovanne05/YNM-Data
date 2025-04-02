from models.transactional.generic_model import GenericModel
from databases.db import db


class Film(GenericModel):
    __tablename__ = 'film'

    idFilm = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('titre.idTitre'), unique=True, nullable=False)
    duree = db.Column(db.Integer)