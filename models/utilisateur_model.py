from models.generic_model import GenericModel
import re

class Utilisateur(GenericModel):
    def __init__(self, idUtilisateur: int, nom: str, prenom: str, age: int,
                 paysResidence: str, email: str, numero: str,
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