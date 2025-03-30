from models.generic_model import GenericModel

class Temps(GenericModel):
    def Temps(self, id_date: int = 0, jour: int = 0, mois: int = 0, annee: int = 0, trimestre: int = 0):
        self.id_date = id_date
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.trimestre = trimestre

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 5:
                self.jour = int(data[2])
                self.mois = int(data[3])
                self.annee = int(data[0])
                self.trimestre = int(data[4])
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError as e:
            raise ValueError("Une des variables n'est pas un entier (seuls des entiers sont requis pour cette table)") from e