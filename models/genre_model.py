from models.generic_model import GenericModel
from databases.db import db


class Genre(GenericModel):
    __tablename__ = 'genre'

    idGenre = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)