from models.generic_model import GenericModel

class Paiement(GenericModel):
    def __init__(self, idPaiement: int, idAbonnement: int, 
                 datePaiement: str, montant: float, 
                 statusPaiement: str):
        self.idPaiement = idPaiement
        self.idAbonnement = idAbonnement
        self.datePaiement = datePaiement
        self.montant = montant
        self.statusPaiement = statusPaiement