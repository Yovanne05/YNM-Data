from models.generic_model import GenericModel
import re

class Utilisateur(GenericModel):
    def __init__(self, idUtilisateur: int = 0, nom: str = "", prenom: str = "", age: int = 0, paysResidence: str = "", email: str = "", numero: str = "",
                 statutAbonnement: str = 'Actif'):
        super().__init__()
        self.idUtilisateur = idUtilisateur
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.paysResidence = paysResidence
        self.email = email
        self.numero = numero
        self.statutAbonnement = statutAbonnement


    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Email invalide")

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 7 and isinstance(data[1], str) and isinstance(data[2], str) and isinstance(data[3], int) and \
                isinstance(data[4], str) and isinstance(data[5], str) and isinstance(data[6], str) and isinstance(
                data[7], str):
                self.nom = data[1]
                self.prenom = data[2]
                self.age = data[3]
                self.paysResidence = data[4]
                self.email = data[5]
                self.numero = data[6]
                self.statutAbonnement = data[7]
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")