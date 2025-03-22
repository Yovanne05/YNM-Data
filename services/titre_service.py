from typing import Any

from models.titre_model import Titre
from models.temps_model import Temps
import db
from utils.categorie_age_titre import categorie_age_autorise


def get_all_titres() -> list[Titre] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM titre")
            result = cursor.fetchall()

        titres = [Titre.from_db(row) for row in result]

        return titres

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des titres: {str(e)}")

    finally:
        con.close()


def get_titre_by_id(id_titre: int) -> list[Titre] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM titre WHERE idTitre=%s", (id_titre,))
            result = cursor.fetchall()

        titre = [Titre.from_db(row) for row in result]

        return titre

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des titres: {str(e)}")

    finally:
        con.close()

def create_titre(titre: Titre) -> None:
    con = db.get_db_connection()

    try:
        if check_coherences_dates(titre.id_date_debut_licence, titre.id_date_fin_licence):
            raise Exception(f"Les dates de licence ne sont pas cohérentes : la date de fin se situe au même jour ou avant la date de début")

        with con.cursor() as cursor:
            cursor.execute("INSERT INTO titre (nom, annee, iddateDebutLicence, iddateFinLicence, idGenre, categorieAge, description) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (titre.nom, titre.annee, titre.id_date_debut_licence, titre.id_date_fin_licence, titre.id_genre, titre.categorie_age, titre.description))

            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout du titre: {str(e)}")

    finally:
        con.close()

def update_titre(titre: Titre, data: Any) -> None:
    con = db.get_db_connection()

    try:
        if data.get("nom"):
            titre.nom = data["nom"]
        if data.get("annee"):
            titre.annee = data["annee"]
        if data.get("iddateDebutLicence"):
            titre.id_date_debut_licence = data["iddateDebutLicence"]
        if data.get("iddateFinLicence"):
            titre.id_date_fin_licence = data["iddateFinLicence"]
        if data.get("idGenre"):
            titre.id_genre = data["idGenre"]
        if data.get("categorieAge") and data["categorieAge"] in categorie_age_autorise:
            titre.categorie_age = data["categorieAge"]
        if data.get("description"):
            titre.description = data["description"]

        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE titre "
                "SET nom = %s, annee = %s, iddateDebutLicence = %s, iddateFinLicence = %s, idGenre = %s, categorieAge = %s, description = %s"
                "WHERE idTitre=%s",
                (titre.nom, titre.annee, titre.id_date_debut_licence, titre.id_date_fin_licence, titre.id_genre,titre.categorie_age, titre.description, titre.id_titre))
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la modification du titre: {str(e)}")

    finally:
        con.close()

def delete_titre(id_titre: int) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM titre WHERE idTitre=%s", (id_titre,))
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression du titre: {str(e)}")

    finally:
        con.close()

def check_coherences_dates(id_date_debut_licence: int, id_date_fin_licence: int) -> bool or None:
    con = db.get_db_connection()

    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM temps WHERE id_date_debutLicence=%s", (id_date_debut_licence,))
            result_debut = cursor.fetchall()
            cursor.execute("SELECT * FROM temps WHERE id_date_finLicence=%s", (id_date_fin_licence,))
            result_fin = cursor.fetchall()

            temps_debut = [Temps.from_db(row) for row in result_debut][0]
            temps_fin = [Temps.from_db(row) for row in result_fin][0]

            if temps_fin.annee > temps_debut.annee:
                return True
            elif temps_fin.annee == temps_debut.annee:
                if temps_fin.mois > temps_debut.mois:
                    return True
                elif temps_fin.mois == temps_debut.mois:
                    if temps_fin.jour > temps_debut.jour:
                        return True

            return False

    except Exception as e:
        raise Exception(f"Erreur lors de la vérification de la cohérence des dates: {str(e)}")

    finally:
        con.close()



# def get_titre_by_id(id_titre: int) -> list[Titre] or None:
#     con = db.get_db_connection()
#     try:
#         with con.cursor() as cursor:
#             cursor.execute("SELECT * FROM titre WHERE idTitre=%s", (id_titre,))
#             result = cursor.fetchall()
#
#         titre = [Titre.from_db(row) for row in result]
#
#         return titre
#
#     except Exception as e:
#         raise Exception(f"Erreur lors de la récupération des titres: {str(e)}")
#
#     finally:
#         con.close()
