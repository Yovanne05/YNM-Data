from utils.statut_utilisateur import statut_autorise
class Utilisateur:
    def __init__(self, idUtilisateur: int, nom: str, prenom: str, age: int, paysResidence: str, email: str, numero: str, statut: str):
        self.idUtilisateur = idUtilisateur
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.paysResidence = paysResidence
        self.email = email
        self.numero = numero
        self.statut = statut

    @classmethod
    def from_db(cls, data):
        statut_abonnement = data['statutAbonnement']

        if statut_abonnement not in statut_autorise :
            raise ValueError(f"Invalid statutAbonnement: {statut_abonnement}")

        return cls(
            idUtilisateur=data['idUtilisateur'],
            nom=data['nom'],
            prenom=data['prenom'],
            age=data['age'],
            paysResidence=data['paysResidence'],
            email=data['email'],
            numero=data['numero'],
            statut=statut_abonnement
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
            'statut_abonnement': self.statut
        }