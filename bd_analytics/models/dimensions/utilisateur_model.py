from databases.db import db

class UtilisateurDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Utilisateur'

    idUtilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    age = db.Column(db.Integer)
    paysResidence = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True, nullable=False)
    numero = db.Column(db.String(15), unique=True, nullable=False)
    statutAbonnement = db.Column(db.String(20), default='Actif')

    _visionnages = db.relationship("VisionnageFact", backref="utilisateur")
    _evaluations = db.relationship("EvaluationFact", backref="utilisateur")
    _paiements = db.relationship("PaiementFact", backref="utilisateur")
