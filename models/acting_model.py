from models.generic_model import GenericModel
from databases.db import db


class Acting(GenericModel):
    __tablename__ = 'acting'

    idActing = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('titre.idTitre'), nullable=False)
    idActeur = db.Column(db.Integer, db.ForeignKey('acteur.idActeur'), nullable=False)
