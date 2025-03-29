from models.generic_model import GenericModel

class Abonnement(GenericModel):
    def __init__(self, idAbonnement: int, typeAbonnement: str, prix: float):
        self.idAbonnement = idAbonnement
        self.typeAbonnement = typeAbonnement
        self.prix = prix
