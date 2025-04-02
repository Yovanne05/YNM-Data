from models.generic_model import GenericModel

class Genre(GenericModel):
    def __init__(self, id_genre: int, nom_genre: str):
        self.id_genre = id_genre
        self.nom_genre = nom_genre