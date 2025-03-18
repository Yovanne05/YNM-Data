from models.utilisateur_model import Utilisateur
import db


def get_all_utilisateurs():
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM Utilisateur")
            result = cursor.fetchall()

        utilisateurs = [Utilisateur.from_db(row) for row in result]

        return utilisateurs

    except Exception as e:
        raise Exception(f"Error fetching utilisateurs: {str(e)}")

    finally:
        con.close()
