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


def update_abonnement(current_data: dict, updated_data: dict) -> bool:
    """
    Met à jour un abonnement dans la base de données
    Args:
        current_data: Données actuelles (doit contenir idAbonnement)
        updated_data: Nouvelles valeurs à mettre à jour
    Returns:
        bool: True si la mise à jour a réussi
    Raises:
        Exception: Si erreur lors de la mise à jour
    """
    con = db.get_db_connection()
    try:
        if 'idAbonnement' not in current_data:
            raise ValueError("ID abonnement manquant dans current_data")

        if current_data['idAbonnement'] != updated_data.get('idAbonnement'):
            raise ValueError("Incohérence d'ID entre current_data et updated_data")

        set_clause = ", ".join([
            f"`{key}` = %s"
            for key in updated_data.keys()
            if key != 'idAbonnement'
        ])

        set_values = [
            updated_data[key]
            for key in updated_data.keys()
            if key != 'idAbonnement'
        ]
        set_values.append(current_data['idAbonnement'])

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
