from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class LangueDisponible(GenericModel):
    __tablename__ = 'langue_disponible'

    idLangueDisponible = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('titre.idTitre', name='fk_langue_disponible_titre'), nullable=False)
    idLangue = db.Column(db.Integer, db.ForeignKey('langue.idLangue', name='fk_langue_disponible_langue'), nullable=False)
    typeLangue = db.Column(db.Enum('audio', 'sous-titre'))
