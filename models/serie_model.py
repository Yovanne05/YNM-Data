class Serie:
    
    def __init__(self, idSerie: int, nom: str, genre: str, saison: int, annee: int, dateDebutLicence: str, dateFinLicence: str, categorieAge: str, description :str):
        self.idSerie = idSerie
        self.nom = nom
        self.genre = genre
        self.saison = saison
        self.annee = annee
        self.dateDebutLicence = dateDebutLicence
        self.dateFinLicence = dateFinLicence
        self.categorieAge = categorieAge
        self.description = description
        
    
    @classmethod
    def from_db(cls, data):
        return cls(
            idSerie=data['idSerie'],
            nom=data['nom'],
            genre=data['genre'],
            saison=data['saison'],
            annee=data['annee'],
            dateDebutLicence=data['dateDebutLicence'],
            dateFinLicence=data['dateFinLicence'],
            categorieAge=data['categorieAge'],
            description=data['description']
        )
        
    def as_dict(self):
        return {
            'idSerie': self.idSerie,
            'nom': self.nom,
            'genre': self.genre,
            'saison': self.saison,
            'annee': self.annee,
            'dateDebutLicence': self.dateDebutLicence,
            'dateFinLicence': self.dateFinLicence,
            'categorieAge': self.categorieAge,
            'description': self.description
        }