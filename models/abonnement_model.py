from models.generic_model import GenericModel

class Abonnement(GenericModel):
    def __init__(self, id_abonnement: int, id_utilisateur: int, type_abonnement: str, prix: float):
        self.id_abonnement = id_abonnement
        self.id_utilisateur = id_utilisateur
        self.type_abonnement = type_abonnement
        self.prix = prix
