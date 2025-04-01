from models.generic_model import GenericModel

class Acteur(GenericModel):
    def __init__(self, id_acteur: int = 0, nom: str = "", prenom: str = "", date_naissance: str = "", date_deces: str = ""):
        self.id_acteur = id_acteur
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.date_deces = date_deces