from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Film(GenericModel):
    __tablename__ = 'Film'

    idFilm = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre', name='fk_film_titre'), nullable=False)
    duree = db.Column(db.Integer)