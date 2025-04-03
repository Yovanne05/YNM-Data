from databases.db import db

class GenreDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Genre'

    idGenre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomGenre = db.Column(db.String(50))
