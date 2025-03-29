from models.generic_model import GenericModel

class Profil(GenericModel):
    def __init__(self, idProfil: int, nom: str, 
                 typeProfil: str, idUtilisateur: int):
        self.idProfil = idProfil
        self.nom = nom
        self.typeProfil = typeProfil
        self.idUtilisateur = idUtilisateur