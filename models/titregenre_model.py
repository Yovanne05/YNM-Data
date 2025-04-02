from models.generic_model import GenericModel

class TitreGenre(GenericModel):
    def __init__(self, id_titre: int, id_genre: int):
        self.id_titre = id_titre
        self.id_genre = id_genre