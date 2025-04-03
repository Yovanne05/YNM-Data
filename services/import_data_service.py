import csv
from typing import List, TypeAlias

from flask import Request

from models.abonnement_model import Abonnement
from models.acteur_model import Acteur
from models.acting_model import Acting
from models.evaluation_model import Evaluation
from models.film_model import Film
from models.genre_model import Genre
from models.langue_model import Langue
from models.languedispo_model import LangueDisponible
from models.maliste_model import MaListe
from models.paiement_model import Paiement
from models.profil_model import Profil
from models.realisation_model import Realisation
from models.serie_model import Serie
from models.studio_model import Studio
from models.titre_model import Titre
from models.titregenre_model import TitreGenre
from models.utilisateur_model import Utilisateur
from services.generic_service import GenericService

MODELS = {
    "abonnement": Abonnement(),
    "acteur": Acteur(),
    "acting": Acting(),
    "evaluation": Evaluation(),
    "film": Film(),
    "genre": Genre(),
    "langue": Langue(),
    "langue_disponible": LangueDisponible(),
    "maliste": MaListe(),
    "paiement": Paiement(),
    "profil": Profil(),
    "realisation": Realisation(),
    "serie": Serie(),
    "studio": Studio(),
    "titre": Titre(),
    "titregenre": TitreGenre(),
    "utilisateur": Utilisateur()
}

SERVICES = {
    "abonnement": GenericService(Abonnement),
    "acteur": GenericService(Acteur),
    "acting": GenericService(Acting),
    "evaluation": GenericService(Evaluation),
    "film": GenericService(Film),
    "genre": GenericService(Genre),
    "langue": GenericService(Langue),
    "langue_disponible": GenericService(LangueDisponible),
    "maliste": GenericService(MaListe),
    "paiement": GenericService(Paiement),
    "profil": GenericService(Profil),
    "realisation": GenericService(Realisation),
    "serie": GenericService(Serie),
    "studio": GenericService(Studio),
    "titre": GenericService(Titre),
    "titregenre": GenericService(TitreGenre),
    "utilisateur": GenericService(Utilisateur),
}

FILE_PATH = "utils/import.csv"

netflix_object: TypeAlias = Abonnement | Genre | Paiement | Serie | Titre | Utilisateur

def save_file(request: Request) -> None:
    file = request.files['file']

    if file.mimetype not in ["text/csv", "application/vnd.ms-excel"]:
        raise Exception("Format de fichier non valide")

    file.save(f"utils/import.csv")


def import_data_to_db(table_name: str) -> None:
    try:
        data = read_data(table_name)
        if table_name in SERVICES:
            for d in data:
                SERVICES[table_name].create(d)
    except Exception as e:
        raise Exception(f"Erreur lors de l'importation dans la base de données : {str(e)}")


def get_instance(table_name: str) -> netflix_object :
    try:
        if table_name not in MODELS.keys():
            raise Exception(f"La table {table_name} n'existe pas")
        model = type(MODELS.get(table_name.lower()))
        return model()
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération de la table d'import: {str(e)}")


def read_data(table_name: str) -> list[dict[str, str]]:
    try:
        separateur = get_separateur(FILE_PATH)
        headers = get_headers(FILE_PATH, separateur)
        if headers:
            if sorted(headers) != sorted(get_instance(table_name).as_dict().keys()):
                raise Exception("Les en-tête du fichier ne correspondent pas aux attributs de la table")
        #TODO: faire en sorte de pouvoir éviter la colonne id
        with open(FILE_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            all_lines = []
            if headers:
                next(reader)
            for row in reader:
                line_dict = dict(zip(sorted(get_instance(table_name).as_dict().keys()), row))
                pop_id(table_name, line_dict)
                all_lines.append(line_dict)
        return all_lines
    except Exception as e:
        raise Exception(e)


def get_separateur(file_path: str) -> str:
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        echantillon = file.read(1024)
        file.seek(0)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(echantillon, delimiters=",;")
        return dialect.delimiter


def get_headers(file_path: str, separateur: str) -> List[str] | None:
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        echantillon = file.read(1024)
        file.seek(0)
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(echantillon)
        reader = csv.reader(file, delimiter=separateur)
        if has_header:
            headers = next(reader, None)
        else:
            headers = None
    return headers

def pop_id(table_name: str, data: dict[str, str]) -> None:
    if table_name != "titregenre":
        string_pop = "id" + "".join(x.capitalize() for x in table_name.lower().split("_"))
        data.pop(string_pop, None)