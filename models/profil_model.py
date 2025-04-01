from models.generic_model import GenericModel

class Profil(GenericModel):
    def __init__(self, id_profil: int, nom: str,
                 type_profil: str, id_utilisateur: int):
        self.id_profil = id_profil
        self.nom = nom
        self.type_profil = type_profil
        self.id_utilisateur = id_utilisateur