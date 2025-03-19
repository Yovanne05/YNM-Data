class Abonnement:
    def __init__(self, idAbonnement: int, typeAbonnement: str, prix: float):
        self.idAbonnement = idAbonnement
        self.typeAbonnement = typeAbonnement
        self.prix = prix
        
        
    @classmethod
    def from_db(cls, data):
        return cls(
            idAbonnement = data['idAbonnement'],
            typeAbonnement = data['typeAbonnement'],
            prix = data['prix']
        )

    def as_dict(self):
        return {
            'idAbonnement': self.idAbonnement,
            'typeAbonnement': self.typeAbonnement,
            'prix': self.prix
        }