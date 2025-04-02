from models.generic_model import GenericModel

class Serie(GenericModel):
    def __init__(self, id_serie: int, id_titre: int, saison: int):
        self.id_serie = id_serie
        self.id_titre = id_titre
        self.saison = saison