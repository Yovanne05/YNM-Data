from utils.categorie_age_titre import categorie_age_autorise

class Titre:
    def __init__(self, id_titre: int, nom: str, annee: int, id_date_debut_licence: int, id_date_fin_licence: int, id_genre: int, categorie_age: str, description: str):
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
