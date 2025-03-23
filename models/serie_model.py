class Serie:
    def __init__(self, idSerie: int, idTitre: int, saison: int):
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