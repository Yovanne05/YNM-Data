from bd_transactional.models.generic_model import GenericModel
from databases.db import db


class Langue(GenericModel):
    __tablename__ = 'langue'

    idLangue = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    languedisponible = db.relationship('LangueDisponible', cascade='all,delete', backref='langues')