from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Acting(GenericModel):
    __tablename__ = 'Acting'

    idActing = db.Column(db.Integer, primary_key=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre', name='fk_acting_titre'), nullable=False)
    idActeur = db.Column(db.Integer, db.ForeignKey('Acteur.idActeur', name='fk_acting_acteur'), nullable=False)

    titre = db.relationship('Titre', backref='actings')
    acteur = db.relationship('Acteur', backref='actings')
