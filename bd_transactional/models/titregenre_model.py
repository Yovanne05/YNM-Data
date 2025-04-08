from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class TitreGenre(GenericModel):
    __tablename__ = 'TitreGenre'

    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre', name='fk_titregenre_titre'), primary_key=True)
    idGenre = db.Column(db.Integer, db.ForeignKey('Genre.idGenre', name='fk_titregenre_genre'), primary_key=True)
