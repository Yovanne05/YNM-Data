from models.generic_model import GenericModel

class Acting(GenericModel):
    def __init__(self, id_acting: int = 0, id_titre: int = 0, id_acteur: int = 0):
        self.id_acting = id_acting
        self.id_titre = id_titre
        self.id_acteur = id_acteur
