from databases.db import db

class EvaluationFact(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Evaluation'

    idEvaluation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUtilisateur = db.Column(db.Integer, db.ForeignKey('Utilisateur.idUtilisateur'))
    idTitre = db.Column(db.Integer, db.ForeignKey('Titre.idTitre'))
    idGenre = db.Column(db.Integer, db.ForeignKey('Genre.idGenre'))
    idDate = db.Column(db.Integer, db.ForeignKey('Temps.idDate'))
    note = db.Column(db.Integer)
