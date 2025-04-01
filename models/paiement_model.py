from models.generic_model import GenericModel

class Paiement(GenericModel):
    def __init__(self, id_paiement: int = 0, id_abonnement: int = 0, date_paiement: int = 0, montant: float = 0, status_paiement: str = ""):
        self.id_paiement = id_paiement
        self.id_abonnement = id_abonnement
        self.date_paiement = date_paiement
        self.montant = montant
        self.status_paiement = status_paiement

    def init_from_list(self, data: list) -> None:
        try:
            self.id_abonnement = int(data[0])
            self.date_paiement = int(data[1])
            self.status_paiement = data[4]
        except IndexError:
            raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")