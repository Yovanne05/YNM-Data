from models.generic_model import GenericModel

class Paiement(GenericModel):
    def __init__(self, idPaiement: int = 0, idAbonnement: int = 0, datePaiement: int = 0, montant: float = 0, statusPaiement: str = ""):
        self.idPaiement = idPaiement
        self.idAbonnement = idAbonnement
        self.datePaiement = datePaiement
        self.montant = montant
        self.statusPaiement = statusPaiement

    def init_from_list(self, data: list) -> None:
        try:
            self.id_utilisateur = int(data[3])
            self.id_abonnement = int(data[0])
            self.id_date = int(data[1])
            self.status_paiement = data[4]
        except IndexError:
            raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")