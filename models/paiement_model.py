from models.generic_model import GenericModel

class Paiement(GenericModel):
    def __init__(self, id_paiement: int, id_abonnement: int,
                 date_paiement: str, montant: float,
                 status_paiement: str):
        self.id_paiement = id_paiement
        self.id_abonnement = id_abonnement
        self.date_paiement = date_paiement
        self.montant = montant
        self.status_paiement = status_paiement