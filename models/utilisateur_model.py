from utils.statut_utilisateur import statut_autorise
class Utilisateur:
    def __init__(self, idUtilisateur: int = 0, nom: str = "", prenom: str = "", age: int = 0, paysResidence: str = "", email: str = "", numero: str = "", statut_abonnement: str = ""):
        self.idUtilisateur = idUtilisateur
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.paysResidence = paysResidence
        self.email = email
        self.numero = numero
        self.statut_abonnement = statut_abonnement

    @classmethod
    def from_db(cls, data):
        statut_abonnement_recu = data['statutAbonnement']

        if statut_abonnement_recu not in statut_autorise :
            raise ValueError(f"Invalid statutAbonnement: {statut_abonnement_recu}")

        return cls(
            idUtilisateur=data['idUtilisateur'],
            nom=data['nom'],
            prenom=data['prenom'],
            age=data['age'],
            paysResidence=data['paysResidence'],
            email=data['email'],
            numero=data['numero'],
            statut_abonnement=statut_abonnement_recu
        )

    def as_dict(self):
        return {
            'idUtilisateur': self.idUtilisateur,
            'nom': self.nom,
            'prenom': self.prenom,
            'age': self.age,
            'paysResidence': self.paysResidence,
            'email': self.email,
            'numero': self.numero,
            'statutAbonnement': self.statut_abonnement
        }

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 7 and isinstance(data[1], str) and isinstance(data[2], str) and isinstance(data[3], int) and \
                isinstance(data[4], str) and isinstance(data[5], str) and isinstance(data[6], str) and isinstance(
                data[7], str):
                self.nom = data[1]
                self.prenom = data[2]
                self.age = data[3]
                self.paysResidence = data[4]
                self.email = data[5]
                self.numero = data[6]
                self.statut_abonnement = data[7]
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")