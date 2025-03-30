class Serie:
    def __init__(self, idSerie: int = 0, idTitre: int = 0, saison: int = 0):
        self.idSerie = idSerie
        self.idTitre = idTitre
        self.saison = saison
    
    @classmethod
    def from_db(cls, data):
        return cls(
            idSerie=data['idSerie'],
            idTitre=data['idTitre'],
            saison=data['saison']
        )
    
    def as_dict(self):
        return {
            'idSerie': self.idSerie,
            'idTitre': self.idTitre,
            'saison': self.saison
        }

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 3 and isinstance(data[1], int) and isinstance(data[2], int):
                self.idTitre = data[1]
                self.saison = data[2]
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")