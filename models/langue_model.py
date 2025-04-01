from models.generic_model import GenericModel

class Langue(GenericModel):
    def __init__(self, id_langue: int = 0, nom: str = ""):
        self.id_langue = id_langue
        self.nom = nom