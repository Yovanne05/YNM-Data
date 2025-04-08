from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Profil(GenericModel):
    __tablename__ = 'Profil'

    idProfil = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    typeProfil = db.Column(db.Enum('Adulte', 'Enfant'), default='Adulte', nullable=False)
    idUtilisateur = db.Column(db.Integer, db.ForeignKey('Utilisateur.idUtilisateur', name='fk_profil_utilisateur'), nullable=False)

    utilisateur = db.relationship('Utilisateur', backref='profils')
