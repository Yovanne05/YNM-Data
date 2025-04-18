from databases.db import db

class TempsDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Temps'

    idDate = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jour = db.Column(db.Integer)
    mois = db.Column(db.Integer)
    annee = db.Column(db.Integer)
    trimestre = db.Column(db.Integer)
    jour_semaine = db.Column(db.Integer)
    est_weekend = db.Column(db.Boolean)

    _visionnages = db.relationship("VisionnageFact", backref="temps")
    _evaluations = db.relationship("EvaluationFact", backref="temps")
    _paiements = db.relationship("PaiementFact", backref="temps")
    _titres_debut = db.relationship("TitreDim", foreign_keys="[TitreDim.iddateDebutLicence]", backref="dateDebutLicence")
    _titres_fin = db.relationship("TitreDim", foreign_keys="[TitreDim.iddateFinLicence]", backref="dateFinLicence")
