from databases.db import db


class Temps(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Temps'

    idDate = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jour = db.Column(db.Integer)
    mois = db.Column(db.Integer)
    annee = db.Column(db.Integer)
    trimestre = db.Column(db.Integer)
