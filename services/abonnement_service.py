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
