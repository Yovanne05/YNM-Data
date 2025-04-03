from databases.db import db

class AbonnementDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Abonnement'

    idAbonnement = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typeAbonnement = db.Column(db.String(50))
    prix = db.Column(db.Numeric(6, 2))

    _paiements = db.relationship("PaiementFact", backref="abonnement")