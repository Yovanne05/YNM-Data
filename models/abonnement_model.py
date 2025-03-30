class Abonnement:
    def __init__(self, idAbonnement: int = 0, typeAbonnement: str = "", prix: float = 0):
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

    def init_from_list(self, data: list[str]) -> None:
        try:
            if isinstance(data[1], str) and isinstance(data[2], float):
                self.typeAbonnement = data[1]
                self.prix = data[2]
        except IndexError:
            raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")