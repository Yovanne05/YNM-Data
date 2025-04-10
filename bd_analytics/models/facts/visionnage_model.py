from sqlalchemy.orm import relationship

from databases.db import db

class VisionnageFact(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Visionnage'

    idVisionnage = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUtilisateur = db.Column(db.Integer, db.ForeignKey('Utilisateur.idUtilisateur'))
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre'))
    idDate = db.Column(db.Integer, db.ForeignKey('Temps.idDate'))
    idGenre = db.Column(db.Integer, db.ForeignKey('Genre.idGenre'))
    idLangueDisponible = db.Column(db.Integer, db.ForeignKey('Langue_Disponible.idLangueDisponible'))
    dureeVisionnage = db.Column(db.Integer)
    nombreVues = db.Column(db.Integer, default=1)