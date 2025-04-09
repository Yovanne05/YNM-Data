from bd_transactional.models.generic_model import GenericModel
from databases.db import db


class Realisation(GenericModel):
    __tablename__ = 'Realisation'

    idRealisation = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre', name='fk_realisation_titre'), nullable=False)
    idStudio = db.Column(db.Integer, db.ForeignKey('Studio.idStudio', name='fk_realisation_studio'), nullable=False)
