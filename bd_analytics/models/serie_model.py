from databases.db import db

class SerieEntrepot(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Serie'

    idSerie = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre'), unique=True, nullable=False)
    saison = db.Column(db.Integer, nullable=False)

    titre = db.relationship("TitreDim", backref="serie", uselist=False)