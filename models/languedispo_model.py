from models.generic_model import GenericModel

class LangueDisponible(GenericModel):
    def LangueDisponible(self, id_languedispo: int, id_titre: int, id_langue: int, type_langue: str):
        self.id_languedispo = id_languedispo
        self.id_titre = id_titre
        self.id_langue = id_langue
        self.type_langue = type_langue