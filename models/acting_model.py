from models.generic_model import GenericModel

class Acting(GenericModel):
    def __init__(self, id_acting: int, id_titre: int, id_acteur: int):
        self.id_acting = id_acting
        self.id_titre = id_titre
        self.id_acteur = id_acteur
