from databases.db import db


class PaiementFact(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Paiement'

    idPaiement = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUtilisateur = db.Column(db.Integer, db.ForeignKey('Utilisateur.idUtilisateur'), nullable=False)
    idAbonnement = db.Column(db.Integer, db.ForeignKey('Abonnement.idAbonnement'), nullable=False)
    idDate = db.Column(db.Integer, db.ForeignKey('Temps.idDate'), nullable=False)
    montant = db.Column(db.Numeric(6, 2))
    statusPaiement = db.Column(db.String(20))
