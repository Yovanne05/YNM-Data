import csv
from typing import List, TypeAlias
from flask import Request
from databases.db import db

from bd_transactional.services.generic_service import GenericService

SERVICES = {
    "abonnement": GenericService(db.models.Abonnement),
    "acteur": GenericService(db.models.Acteur),
    "acting": GenericService(db.models.Acting),
    "evaluation": GenericService(db.models.Evaluation),
    "film": GenericService(db.models.Film),
    "genre": GenericService(db.models.Genre),
    "langue": GenericService(db.models.Langue),
    "langue_disponible": GenericService(db.models.LangueDisponible),
    "maliste": GenericService(db.models.MaListe),
    "paiement": GenericService(db.models.Paiement),
    "profil": GenericService(db.models.Profil),
    "realisation": GenericService(db.models.Realisation),
    "serie": GenericService(db.models.Serie),
    "studio": GenericService(db.models.Studio),
    "titre": GenericService(db.models.Titre),
    "titregenre": GenericService(db.models.TitreGenre),
    "utilisateur": GenericService(db.models.Utilisateur),
}

FILE_PATH = "utils/import.csv"

netflix_object: TypeAlias = db.models.Abonnement | db.models.Genre | db.models.Paiement | db.models.Serie | db.models.Titre | db.models.Utilisateur

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
        if table_name not in db.models:
            raise Exception(f"La table {table_name} n'existe pas")
        model = type(db.models.get(table_name.lower()))
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