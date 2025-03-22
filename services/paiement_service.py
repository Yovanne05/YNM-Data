from typing import Any
from models.paiement_model import Paiement
import db

def get_all_paiements() -> list[Paiement] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM paiement")
            result = cursor.fetchall()

        paiements = [Paiement.from_db(row) for row in result]
        return paiements
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des paiements: {str(e)}")
    finally:
        con.close()

def get_paiement_by_id(id_paiement: int) -> list[Paiement] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM paiement WHERE idPaiement=%s", (id_paiement,))
            result = cursor.fetchall()

        paiement = [Paiement.from_db(row) for row in result]
        return paiement
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération du paiement: {str(e)}")
    finally:
        con.close()

def create_paiement(paiement: Paiement) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute(
                "INSERT INTO paiement (idUtilisateur, idAbonnement, idDate, statusPaiement) "
                "VALUES (%s, %s, %s, %s)",
                (paiement.id_utilisateur, paiement.id_abonnement, paiement.id_date, paiement.status_paiement)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout du paiement: {str(e)}")
    finally:
        con.close()

def update_paiement(paiement: Paiement, data: Any) -> None:
    con = db.get_db_connection()
    try:
        if data.get("idUtilisateur"):
            paiement.id_utilisateur = data["idUtilisateur"]
        if data.get("idAbonnement"):
            paiement.id_abonnement = data["idAbonnement"]
        if data.get("idDate"):
            paiement.id_date = data["idDate"]
        if data.get("statusPaiement"):
            paiement.status_paiement = data["statusPaiement"]

        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE paiement SET idUtilisateur = %s, idAbonnement = %s, idDate = %s, statusPaiement = %s "
                "WHERE idPaiement = %s",
                (paiement.id_utilisateur, paiement.id_abonnement, paiement.id_date, paiement.status_paiement, paiement.id_paiement)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la modification du paiement: {str(e)}")
    finally:
        con.close()

def delete_paiement(id_paiement: int) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM paiement WHERE idPaiement=%s", (id_paiement,))
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression du paiement: {str(e)}")
    finally:
        con.close()
