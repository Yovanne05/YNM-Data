from models.generic_model import GenericModel

class Titre(GenericModel):
    def __init__(self, idTitre: int, nom: str, annee: int,
                 dateDebutLicence: str, dateFinLicence: str,
                 categorieAge: str, description: str = None):
        self.idTitre = idTitre
        self.nom = nom
        self.annee = annee
        self.dateDebutLicence = dateDebutLicence
        self.dateFinLicence = dateFinLicence
        self.categorieAge = categorieAge
        self.description = description