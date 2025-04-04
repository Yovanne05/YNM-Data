from databases.db import db

class LangueDisponibleDim(db.Model):
    __bind_key__ = 'entrepot'
    __tablename__ = 'Langue_Disponible'

    idLangueDisponible = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idLangue = db.Column(db.Integer, db.ForeignKey('Langue.idLangue'), nullable=False)
    typeLangue = db.Column(db.String(15))

    _visionnages = db.relationship("VisionnageFact", backref="langue_disponible")
