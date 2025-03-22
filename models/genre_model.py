class Genre:
    def __init__(self, id_genre: int, nom_genre: str):
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