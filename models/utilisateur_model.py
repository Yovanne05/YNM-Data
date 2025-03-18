from utils.statut_utilisateur import statut_autorise
class Utilisateur:
    def __init__(self, id_utilisateur: int, nom: str, prenom: str, age: int, pays_residence: str, email: str, numero: str, statut: str):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.pays_residence = pays_residence
        self.email = email
        self.numero = numero
        self.statut = statut

    @classmethod
    def from_db(cls, data):
        statut_abonnement = data['statutAbonnement']

        if statut_abonnement not in statut_autorise :
            raise ValueError(f"Invalid statutAbonnement: {statut_abonnement}")

        return cls(
            id_utilisateur=data['idUtilisateur'],
            nom=data['nom'],
            prenom=data['prenom'],
            age=data['age'],
            pays_residence=data['paysResidence'],
            email=data['email'],
            numero=data['numero'],
            statut=statut_abonnement
        )

    def as_dict(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'nom': self.nom,
            'prenom': self.prenom,
            'age': self.age,
            'pays_residence': self.pays_residence,
            'email': self.email,
            'numero': self.numero,
            'statut_abonnement': self.statut
        }