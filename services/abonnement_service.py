from models.abonnement_model import Abonnement
import db

def get_all_abonnements():
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM Abonnement")
            result = cursor.fetchall()

        abonnements = [Abonnement.from_db(row) for row in result]

        return abonnements

    except Exception as e: 
        raise Exception(f"Error fetching utilisateurs: {str(e)}")

    finally:
        con.close()


def update_abonnement(id_abonnement: int, updated_data: dict) -> bool:
    """
    Met à jour un abonnement dans la base de données
    Args:
        id_abonnement: ID de l'abonnement à mettre à jour
        updated_data: Nouvelles valeurs à mettre à jour
    Returns:
        bool: True si la mise à jour a réussi, False sinon
    Raises:
        ValueError: Si l'ID est invalide ou si aucune donnée à mettre à jour
        Exception: Si erreur lors de la mise à jour
    """
    con = db.get_db_connection()
    try:
        if not id_abonnement or id_abonnement <= 0:
            raise ValueError("ID abonnement invalide")

        if not updated_data:
            raise ValueError("Aucune donnée à mettre à jour fournie")

        updated_data.pop('idAbonnement', None)

        set_clause = ", ".join([
            f"`{key}` = %s"
            for key in updated_data.keys()
        ])

        set_values = list(updated_data.values())
        set_values.append(id_abonnement)

        with con.cursor() as cursor:
            query = f"""
                UPDATE Abonnement 
                SET {set_clause}
                WHERE idAbonnement = %s
            """
            cursor.execute(query, tuple(set_values))
            con.commit()

            if cursor.rowcount == 0:
                raise ValueError("Aucun abonnement trouvé avec cet ID")

            return True

    except Exception as e:
        con.rollback()
        raise Exception(f"Erreur lors de la mise à jour: {str(e)}")
    finally:
        con.close()