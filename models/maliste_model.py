from models.generic_model import GenericModel

class MaListe(GenericModel):
    def MaListe(self, id_maliste: int, id_profil: int, id_titre: int):
        self.id_maliste = id_maliste
        self.id_profil = id_profil
        self.id_titre = id_titre