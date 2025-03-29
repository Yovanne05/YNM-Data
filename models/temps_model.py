from models.generic_model import GenericModel

class Temps(GenericModel):
    def Temps(self, id_date: int, jour: int, mois: int, annee: int, trimestre: int):
        self.id_date = id_date
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.trimestre = trimestre