from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Serie(GenericModel):
    __tablename__ = 'Serie'

    idSerie = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre', name='fk_serie_titre'), unique=True, nullable=False)
    saison = db.Column(db.Integer)
