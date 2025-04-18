from databases.db import db

class TitreDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Titre'

    idTitre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255))
    annee = db.Column(db.Integer)
    iddateDebutLicence = db.Column(db.Integer, db.ForeignKey('Temps.idDate'))
    iddateFinLicence = db.Column(db.Integer, db.ForeignKey('Temps.idDate'))
    categorieAge = db.Column(db.String(50))
    typeTitre = db.Column(db.String(10))
    description = db.Column(db.Text)
    idGenre = db.Column(db.Integer, db.ForeignKey('Genre.idGenre'))

    _visionnages = db.relationship("VisionnageFact", backref="titre")
    _evaluations = db.relationship("EvaluationFact", backref="titre")
