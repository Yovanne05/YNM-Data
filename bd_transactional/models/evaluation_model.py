from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Evaluation(GenericModel):
    __tablename__ = 'Evaluation'

    idEvaluation = db.Column(db.Integer, primary_key=True)
    idProfil = db.Column(db.Integer, db.ForeignKey('Profil.idProfil', name='fk_evaluation_profil'), nullable=False)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre', name='fk_evaluation_titre'), nullable=False)
    note = db.Column(db.Integer)
    avis = db.Column(db.Text)
