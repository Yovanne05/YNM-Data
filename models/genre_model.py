from models.generic_model import GenericModel

class Genre(GenericModel):
    def __init__(self, idGenre: int = 0, nomGenre: str = ""):
        self.idGenre = idGenre
        self.nomGenre = nomGenre

    def init_from_list(self, data: list[str]) -> None:
        try:
            if isinstance(data[1], str):
                self.nomGenre = data[1]
        except IndexError:
            raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")