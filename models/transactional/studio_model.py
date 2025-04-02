from models.transactional.generic_model import GenericModel
from databases.db import db


class Studio(GenericModel):
    __tablename__ = 'studio'

    idStudio = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), unique=True, nullable=False)
    pays = db.Column(db.String(100), nullable=False)