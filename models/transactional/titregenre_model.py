from models.transactional.generic_model import GenericModel
from databases.db import db


class TitreGenre(GenericModel):
    __tablename__ = 'titregenre'

    idTitre = db.Column(db.Integer, db.ForeignKey('titre.idTitre'), primary_key=True)
    idGenre = db.Column(db.Integer, db.ForeignKey('genre.idGenre'), primary_key=True)