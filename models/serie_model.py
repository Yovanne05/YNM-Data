from models.generic_model import GenericModel

class Serie(GenericModel):
    def Serie(self, id_serie: int = 0, id_titre: int = 0, saison: int = 0):
        self.id_serie = id_serie
        self.id_titre = id_titre
        self.saison = saison

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 3 and isinstance(data[1], int) and isinstance(data[2], int):
                self.idTitre = data[1]
                self.saison = data[2]
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")