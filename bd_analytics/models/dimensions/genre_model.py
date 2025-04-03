from databases.db import db

class GenreDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Genre'

    idGenre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomGenre = db.Column(db.String(50))

    _titres = db.relationship("TitreDim", backref="genre")
    _visionnages = db.relationship("VisionnageFact", backref="genre")
    _evaluations = db.relationship("EvaluationFact", backref="genre")