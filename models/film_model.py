from models.generic_model import GenericModel

class Film(GenericModel):
    def __init__(self, id_film: int = 0, id_titre: int = 0, duree: int = 0):
        self.id_film = id_film
        self.id_titre = id_titre
        self.duree = duree