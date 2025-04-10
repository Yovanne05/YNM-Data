from bd_transactional.models.generic_model import GenericModel
from databases.db import db


class MaListe(GenericModel):
    __tablename__ = 'maliste'

    idMaListe = db.Column(db.Integer, primary_key=True)
    idProfil = db.Column(db.Integer, db.ForeignKey('profil.idProfil', ondelete='CASCADE'), nullable=False)
    idTitre = db.Column(db.Integer, db.ForeignKey('titre.idTitre'), nullable=False)