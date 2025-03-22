from typing import Any

from models.temps_model import Temps
import db

def get_all_temps() -> list[Temps] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM temps")
            result = cursor.fetchall()

        temps = [Temps.from_db(row) for row in result]

        return temps

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des temps: {str(e)}")

    finally:
        con.close()

def get_temps_by_id(id_date: int) -> list[Temps] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM temps WHERE idDate=%s", (id_date,))
            result = cursor.fetchall()

        temps = [Temps.from_db(row) for row in result]

        return temps

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération du temps: {str(e)}")

    finally:
        con.close()

def create_temps(temps: Temps) -> None:
    con = db.get_db_connection()

    try:
        with con.cursor() as cursor:
            cursor.execute("INSERT INTO temps (jour, mois, annee, trimestre) VALUES (%s, %s, %s, %s)",
                           (temps.jour, temps.mois, temps.annee, temps.trimestre))

            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout du temps: {str(e)}")

    finally:
        con.close()

def update_temps(temps: Temps, data: Any) -> None:
    con = db.get_db_connection()

    try:
        if data.get("jour"):
            temps.jour = data["jour"]
        if data.get("mois"):
            temps.mois = data["mois"]
        if data.get("annee"):
            temps.annee = data["annee"]
        if data.get("trimestre"):
            temps.trimestre = data["trimestre"]

        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE temps SET jour = %s, mois = %s, annee = %s, trimestre = %s WHERE idDate=%s",
                (temps.jour, temps.mois, temps.annee, temps.trimestre, temps.id_date)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la modification du temps: {str(e)}")

    finally:
        con.close()

def delete_temps(id_date: int) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM temps WHERE idDate=%s", (id_date,))
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression du temps: {str(e)}")

    finally:
        con.close()