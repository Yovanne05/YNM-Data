from bd_transactional.models.generic_model import GenericModel
from databases.db import db


class Genre(GenericModel):
    __tablename__ = 'Genre'

    idGenre = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    titregenre = db.relationship('TitreGenre', cascade='all,delete', backref='genres')