from models.generic_model import GenericModel

class LangueDisponible(GenericModel):
    def __init__(self, id_langue_disponible: int, id_titre: int, id_langue: int, type_langue: str):
        self.id_langue_disponible = id_langue_disponible
        self.id_titre = id_titre
        self.id_langue = id_langue
        self.type_langue = type_langue