from models.generic_model import GenericModel

class Film(GenericModel):
    def Film(self, id_film: int, id_titre: int, duree: int):
        self.id_film = id_film
        self.id_titre = id_titre
        self.duree = duree