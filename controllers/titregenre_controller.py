from typing import Any
from models.maliste_model import MaListe
import db

def get_all_malistes() -> list[MaListe] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM MaListe")
            result = cursor.fetchall()
        malistes = [MaListe.from_db(row) for row in result]
        return malistes
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des listes: {str(e)}")
    finally:
        con.close()

def get_maliste_by_id(id_maliste: int) -> list[MaListe] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM MaListe WHERE idMaListe=%s", (id_maliste,))
            result = cursor.fetchall()
        maliste = [MaListe.from_db(row) for row in result]
        return maliste
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération de la liste: {str(e)}")
    finally:
        con.close()

def create_maliste(maliste: MaListe) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute(
                "INSERT INTO MaListe (idProfil, idTitre) VALUES (%s, %s)",
                (maliste.id_profil, maliste.id_titre)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout à la liste: {str(e)}")
    finally:
        con.close()

def update_maliste(maliste: MaListe, data: Any) -> None:
    con = db.get_db_connection()
    try:
        if data.get("idProfil"):
            maliste.id_profil = data["idProfil"]
        if data.get("idTitre"):
            maliste.id_titre = data["idTitre"]

        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE MaListe SET idProfil = %s, idTitre = %s WHERE idMaListe = %s",
                (maliste.id_profil, maliste.id_titre, maliste.id_maliste)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la modification de la liste: {str(e)}")
    finally:
        con.close()

def delete_maliste(id_maliste: int) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM MaListe WHERE idMaListe=%s", (id_maliste,))
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression de la liste: {str(e)}")
    finally:
        con.close()