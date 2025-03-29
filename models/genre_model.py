from models.generic_model import GenericModel

class Genre(GenericModel):
    def Genre(self, id_genre: int, nom_genre: str):
        self.id_genre = id_genre
        self.nom_genre = nom_genre