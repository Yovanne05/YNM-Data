from models.generic_model import GenericModel

class Realisation(GenericModel):
    def Realisation(self, id_realisation: int, id_titre: int, id_studio: int):
        self.id_realisation = id_realisation
        self.id_titre = id_titre
        self.id_studio = id_studio