from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Abonnement(GenericModel):
    __tablename__ = 'abonnement'

    idAbonnement = db.Column(db.Integer, primary_key=True)
    idUtilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.idUtilisateur'), unique=True, nullable=False)
    typeAbonnement = db.Column(db.Enum('Basic', 'Standard', 'Premium'), nullable=False)
    prix = db.Column(db.Numeric(6, 2), nullable=False)

    utilisateur = db.relationship('Utilisateur', cascade='all,delete', backref='abonnements')
    paiements = db.relationship('Paiement', backref='abonnement', cascade='all,delete')
