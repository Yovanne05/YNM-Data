from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class MaListe(GenericModel):
    __tablename__ = 'MaListe'

    idMaListe = db.Column(db.Integer, primary_key=True)
    idProfil = db.Column(db.Integer, db.ForeignKey('Profil.idProfil', name='fk_maliste_profil'), nullable=False)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre', name='fk_maliste_titre'), nullable=False)
