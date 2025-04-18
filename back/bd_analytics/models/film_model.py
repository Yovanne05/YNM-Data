from databases.db import db

class FilmEntrepot(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Film'

    idFilm = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre'), unique=True, nullable=False)
    duree = db.Column(db.Integer, nullable=False)

    titre = db.relationship("TitreDim", backref="film", uselist=False)