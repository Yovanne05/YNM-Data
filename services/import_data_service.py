import csv
from typing import List, TypeAlias
import re

from flask import Request

from models.abonnement_model import Abonnement
from models.genre_model import Genre
from models.paiement_model import Paiement
from models.serie_model import Serie
from models.temps_model import Temps
from models.titre_model import Titre
from models.utilisateur_model import Utilisateur
import services.generic_service as generic_service

MODELS = {
    "abonnement": Abonnement(),
    "genre": Genre(),
    "paiement": Paiement(),
    "serie": Serie(),
    "temps": Temps(),
    "titre": Titre(),
    "utilisateur": Utilisateur()
}

SERVICES = {
    # "abonnement": create_abonnement,
    "genre": generic_service.GenericService("genre", Genre).create,
    "paiement": generic_service.GenericService("paiement", Paiement).create,
    # "serie": create_serie,
    "temps": generic_service.GenericService("temps", Temps).create,
    "titre": generic_service.GenericService("titre", Titre).create,
    # "utilisateur": create_utilisateur,
}

FILE_PATH = "utils/import.csv"

netflix_object: TypeAlias = Abonnement | Genre | Paiement | Serie | Temps | Titre | Utilisateur

def save_file(request: Request) -> None:
    file = request.files['file']

    if file.mimetype not in ["text/csv", "application/vnd.ms-excel"]:
        raise Exception("Format de fichier non valide")

    file.save(f"utils/import.csv")


def import_data_to_db(table_name: str) -> None:
    print("1")
    model = get_instance(table_name)
    print("2")
    data = read_data(model, table_name)
    print("3")
    if table_name in SERVICES:
        for d in data:
            print("Ah ouais ?")
            print(d.as_dict())
            SERVICES[table_name](d.as_dict())


def get_instance(table_name: str) -> netflix_object :
    try:
        if table_name not in MODELS.keys():
            raise Exception(f"La table {table_name} n'existe pas")
        model = type(MODELS.get(table_name.lower()))
        return model()
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération de la table d'import: {str(e)}")


def read_data(model: netflix_object, table_name: str) -> list[netflix_object]:
    try:
        separateur = get_separateur(FILE_PATH)
        headers = get_headers(FILE_PATH, separateur)
        if headers:
            if sorted(headers) != sorted(vars(model).keys()):
                print(sorted(headers))
                print(sorted(vars(model).keys()))
                raise Exception("Les en-tête du fichier ne correspondent pas aux attributs de la table")
        #TODO: faire en sorte de pouvoir éviter la colonne id
        with open(FILE_PATH, mode="r", encoding="utf-8") as file:
            print("c'est l'exception")
            reader = csv.reader(file)
            all_lines = []
            if headers:
                next(reader)
            for row in reader:
                all_lines.append(init_object(table_name, row))
        return all_lines
    except Exception as e:
        print(str(e))
        raise Exception(e)


def init_object(table_name: str ,data : list[str]) -> netflix_object:
    new_model = get_instance(table_name)
    new_model.init_from_list(data)
    return new_model


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