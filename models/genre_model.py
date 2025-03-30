class Genre:
    def __init__(self, id_genre: int = 0, nom_genre: str = ""):
        self.id_genre = id_genre
        self.nom_genre = nom_genre

    @classmethod
    def from_db(cls, data):
        return cls(
            id_genre=data["idGenre"],
            nom_genre=data["nomGenre"]
        )

    @classmethod
    def from_db_add(cls, data):
        return cls(
            id_genre=0,
            nom_genre=data["nomGenre"]
        )

    def as_dict(self):
        return {
            "id_genre": self.id_genre,
            "nom_genre": self.nom_genre
        }

    def init_from_list(self, data: list[str]) -> None:
        try:
            if isinstance(data[1], str):
                self.nom_genre = data[1]
        except IndexError:
            raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")



