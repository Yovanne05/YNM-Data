from utils.categorie_age_titre import categorie_age_autorise

class Titre:
    def __init__(self, id_titre: int = 0, nom: str = 0, annee: int = 0, id_date_debut_licence: int = 0, id_date_fin_licence: int = 0, id_genre: int = 0, categorie_age: str = "", description: str = ""):
        self.id_titre = id_titre
        self.nom = nom
        self.annee = annee
        self.id_date_debut_licence = id_date_debut_licence
        self.id_date_fin_licence = id_date_fin_licence
        self.id_genre = id_genre
        self.categorie_age = categorie_age
        self.description = description

    @classmethod
    def from_db(cls, data):
        categorie_age = data["categorieAge"]

        if categorie_age not in categorie_age_autorise:
            raise ValueError(f"Mauvaise catégorie d'âge: {categorie_age}" + "\n Catégories possibles : Tout public - 12+ - 16+ - 18+")

        # TODO: Faire un check pour voir si l'année de début de licence <= année de fin de licence

        return cls(
            id_titre=data["idTitre"],
            nom=data["nom"],
            annee=data["annee"],
            id_date_debut_licence=data["iddateDebutLicence"],
            id_date_fin_licence=data["iddateFinLicence"],
            id_genre=data["idGenre"],
            categorie_age=categorie_age,
            description=data["description"]
        )

    @classmethod
    def from_db_add(cls, data):
        categorie_age = data["categorieAge"]

        if categorie_age not in categorie_age_autorise:
            raise ValueError(
                f"Mauvaise catégorie d'âge: {categorie_age}" + "\n Catégories possibles : Tout public - 12+ - 16+ - 18+")

        # TODO: Faire un check pour voir si l'année de début de licence <= année de fin de licence

        return cls(
            id_titre=0,
            nom=data["nom"],
            annee=data["annee"],
            id_date_debut_licence=data["iddateDebutLicence"],
            id_date_fin_licence=data["iddateFinLicence"],
            id_genre=data["idGenre"],
            categorie_age=categorie_age,
            description=data["description"]
        )

    def as_dict(self):
        return {
            "id_titre": self.id_titre,
            "nom": self.nom,
            "annee": self.annee,
            "id_date_debut_licence": self.id_date_debut_licence,
            "id_date_fin_licence": self.id_date_fin_licence,
            "id_genre": self.id_genre,
            "categorie_age": self.categorie_age,
            "description": self.description
        }

    def init_from_list(self, data: list) -> None:
        try:
            if len(data) >= 8:
                print(data)
                self.nom = data[7]
                self.annee = int(data[0])
                self.id_date_debut_licence = int(data[3])
                self.id_date_fin_licence = int(data[4])
                self.id_genre = int(data[5])
                self.categorie_age = data[1]
                self.description = data[2]
                print("ça passe hein")
            else:
                raise IndexError("Une des lignes du fichier CSV n'a pas assez de colonnes")
        except TypeError:
            raise TypeError("Une des variables n'a pas le type demandé")