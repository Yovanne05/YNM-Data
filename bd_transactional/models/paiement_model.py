from bd_transactional.models.generic_model import GenericModel
from databases.db import db

class Paiement(GenericModel):
    __tablename__ = 'paiement'

    idPaiement = db.Column(db.Integer, primary_key=True)
    idAbonnement = db.Column(db.Integer, db.ForeignKey('abonnement.idAbonnement', name='fk_paiement_abonnement'), nullable=False)
    datePaiement = db.Column(db.Date, nullable=False)
    montant = db.Column(db.Numeric(6, 2), nullable=False)
    statusPaiement = db.Column(db.Enum('Effectué', 'Échoué'))
    abonnement = db.relationship('Abonnement', backref='paiements')
