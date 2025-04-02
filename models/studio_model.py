from models.generic_model import GenericModel

class Studio(GenericModel):
    def __init__(self, id_studio: int, nom: str, pays: str):
        self.id_studio = id_studio
        self.nom = nom
        self.pays = pays