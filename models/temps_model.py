class Temps:
    def __init__(self, id_date: int, jour: int, mois: int, annee: int, trimestre: int):
        self.id_date = id_date
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.trimestre = trimestre

    @classmethod
    def from_db(cls, data):
        #TODO : RAJOUTER UN CHECK POUR LES DATES

        return cls(
            id_date=data["idDate"],
            jour=data["jour"],
            mois=data["mois"],
            annee=data["annee"],
            trimestre=data["trimestre"]
        )

    @classmethod
    def from_db_add(cls, data):
        return cls(
            id_date=0,
            jour=data["jour"],
            mois=data["mois"],
            annee=data["annee"],
            trimestre=data["trimestre"]
        )

    def as_dict(self):
        return {
            "id_date": self.id_date,
            "jour": self.jour,
            "mois": self.mois,
            "annee": self.annee,
            "trimestre": self.trimestre
        }
