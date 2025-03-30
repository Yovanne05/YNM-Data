class Paiement:
    def __init__(self, id_paiement: int = 0, id_utilisateur: int = 0, id_abonnement: int = 0, id_date: int = 0, status_paiement: str = ""):
        self.id_paiement = id_paiement
        self.id_utilisateur = id_utilisateur
        self.id_abonnement = id_abonnement
        self.id_date = id_date
        self.status_paiement = status_paiement

    @classmethod
    def from_db(cls, data):
        return cls(
            id_paiement=data["idPaiement"],
            id_utilisateur=data["idUtilisateur"],
            id_abonnement=data["idAbonnement"],
            id_date=data["idDate"],
            status_paiement=data["statusPaiement"]
        )

    @classmethod
    def from_db_add(cls, data):
        return cls(
            id_paiement=0,
            id_utilisateur=data["idUtilisateur"],
            id_abonnement=data["idAbonnement"],
            id_date=data["idDate"],
            status_paiement=data["statusPaiement"]
        )

    def as_dict(self):
        return {
            "id_paiement": self.id_paiement,
            "id_utilisateur": self.id_utilisateur,
            "id_abonnement": self.id_abonnement,
            "id_date": self.id_date,
            "status_paiement": self.status_paiement
        }

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
