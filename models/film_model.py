from models.generic_model import GenericModel

class Film(GenericModel):
    def __init__(self, id_film: int, id_titre: int, duree: int):
        self.id_film = id_film
        self.id_titre = id_titre
        self.duree = duree