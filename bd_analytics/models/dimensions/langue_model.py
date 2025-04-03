from databases.db import db

class LangueDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Langue'

    idLangue = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomLangue = db.Column(db.String(50))
