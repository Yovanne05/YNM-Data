from models.generic_model import GenericModel
import re

class Utilisateur(GenericModel):
    def __init__(self, id_utilisateur: int, nom: str, prenom: str, age: int,
                 pays_residance: str, email: str, numero: str,
                 statut_abonnement: str = 'Actif'):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.pays_residance = pays_residance
        self.email = email
        self.numero = numero
        self.statut_abonnement = statut_abonnement


    def validate_email(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Email invalide")