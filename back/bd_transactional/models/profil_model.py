from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Profil(GenericModel):
    __tablename__ = 'profil'

    idProfil = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    typeProfil = db.Column(db.Enum('Adulte', 'Enfant'), default='Adulte', nullable=False)
    idUtilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.idUtilisateur'), nullable=False)

    evaluations = db.relationship('Evaluation', backref='profil', cascade='all,delete')
    listes = db.relationship('MaListe', backref='profil', cascade='all,delete')