from models.transactional.generic_model import GenericModel
from databases.db import db


class Realisation(GenericModel):
    __tablename__ = 'realisation'

    idRealisation = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('titre.idTitre'), nullable=False)
    idStudio = db.Column(db.Integer, db.ForeignKey('studio.idStudio'), nullable=False)