from models.generic_model import GenericModel

class Evaluation(GenericModel):
    def Evaluation(self, id_evaluation: int, id_profil: int, id_titre: int, note: int, avis: str = None):
        self.id_evaluation = id_evaluation
        self.id_profil = id_profil
        self.id_titre = id_titre
        self.note = note
        self.avis = avis