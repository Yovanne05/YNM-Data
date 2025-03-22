class Paiement:
    def __init__(self, id_paiement: int, id_utilisateur: int, id_abonnement: int, id_date: int, status_paiement: str):
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