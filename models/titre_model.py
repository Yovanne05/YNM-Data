from models.generic_model import GenericModel

class Titre(GenericModel):
    def __init__(self, id_titre: int = 0, nom: str = 0, annee: int = 0, date_debut_licence: int = 0, date_fin_licence: int = 0, categorie_age: str = "", description: str = ""):
        self.id_titre = id_titre
        self.nom = nom
        self.annee = annee
        self.date_debut_licence = date_debut_licence
        self.date_fin_licence = date_fin_licence
        self.categorie_age = categorie_age
        self.description = description

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 8:
                self.nom = data[7]
                self.annee = int(data[0])
                self.date_debut_licence = data[3]
                self.date_fin_licence = data[4]
                self.categorie_age = data[1]
                self.description = data[2]
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")