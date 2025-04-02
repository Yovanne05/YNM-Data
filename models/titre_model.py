from models.generic_model import GenericModel

class Titre(GenericModel):
    def __init__(self, id_titre: int, nom: str, annee: int,
                 date_debut_licence: str, date_fin_licence: str,
                 categorie_age: str, description: str = None):
        self.id_titre = id_titre
        self.nom = nom
        self.annee = annee
        self.date_debut_licence = date_debut_licence
        self.date_fin_licence = date_fin_licence
        self.categorie_age = categorie_age
        self.description = description