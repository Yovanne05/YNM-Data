from models.generic_model import GenericModel

class Titre(GenericModel):
    def __init__(self, idTitre: int = 0, nom: str = 0, annee: int = 0, dateDebutLicence: int = 0, dateFinLicence: int = 0, categorieAge: str = "", description: str = ""):
        self.idTitre = idTitre
        self.nom = nom
        self.annee = annee
        self.dateDebutLicence = dateDebutLicence
        self.dateFinLicence = dateFinLicence
        self.categorieAge = categorieAge
        self.description = description

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 8:
                print(data)
                self.nom = data[7]
                self.annee = int(data[0])
                self.id_date_debut_licence = int(data[3])
                self.id_date_fin_licence = int(data[4])
                self.id_genre = int(data[5])
                self.categorie_age = data[1]
                self.description = data[2]
                print("ça passe hein")
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")