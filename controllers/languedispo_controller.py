from typing import Any
from models.langue_model import Langue
import db

def get_all_langues() -> list[Langue] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM Langue")
            result = cursor.fetchall()
        langues = [Langue.from_db(row) for row in result]
        return langues
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des langues: {str(e)}")
    finally:
        con.close()

def get_langue_by_id(id_langue: int) -> list[Langue] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM Langue WHERE idLangue=%s", (id_langue,))
            result = cursor.fetchall()
        langue = [Langue.from_db(row) for row in result]
        return langue
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération de la langue: {str(e)}")
    finally:
        con.close()

def create_langue(langue: Langue) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Langue (nom) VALUES (%s)",
                (langue.nom,)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout de la langue: {str(e)}")
    finally:
        con.close()

def update_langue(langue: Langue, data: Any) -> None:
    con = db.get_db_connection()
    try:
        if data.get("nom"):
            langue.nom = data["nom"]

        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE Langue SET nom = %s WHERE idLangue = %s",
                (langue.nom, langue.id_langue)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la modification de la langue: {str(e)}")
    finally:
        con.close()

def delete_langue(id_langue: int) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM Langue WHERE idLangue=%s", (id_langue,))
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression de la langue: {str(e)}")
    finally:
        con.close()