from models.generic_model import GenericModel

class Abonnement(GenericModel):
    def __init__(self, id_abonnement: int = 0, type_abonnement: str = "", prix: float = 0):
        self.id_abonnement = id_abonnement
        self.type_abonnement = type_abonnement
        self.prix = prix

    def init_from_list(self, data: list[str]) -> None:
        try:
            if isinstance(data[1], str) and isinstance(data[2], float):
                self.type_abonnement = data[1]
                self.prix = data[2]
        except IndexError:
            raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")