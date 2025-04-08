from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Evaluation(GenericModel):
    __tablename__ = 'evaluation'

    idEvaluation = db.Column(db.Integer, primary_key=True)
    idProfil = db.Column(db.Integer, db.ForeignKey('profil.idProfil', name='fk_evaluation_profil'), nullable=False)
    idTitre = db.Column(db.Integer, db.ForeignKey('titre.idTitre', name='fk_evaluation_titre'), nullable=False)
    note = db.Column(db.Integer)
    avis = db.Column(db.Text)
