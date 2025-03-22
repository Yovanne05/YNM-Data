from typing import Any

from models.genre_model import Genre
import db

def get_all_genres() -> list[Genre] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM genre")
            result = cursor.fetchall()

        genres = [Genre.from_db(row) for row in result]

        return genres

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des genres: {str(e)}")

    finally:
        con.close()

def get_genre_by_id(id_genre: int) -> list[Genre] or None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT * FROM genre WHERE idGenre=%s", (id_genre,))
            result = cursor.fetchall()

        genre = [Genre.from_db(row) for row in result]

        return genre

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération du genre: {str(e)}")

    finally:
        con.close()

def create_genre(genre: Genre) -> None:
    con = db.get_db_connection()

    try:
        with con.cursor() as cursor:
            cursor.execute("INSERT INTO genre (nomGenre) VALUES (%s)", (genre.nom_genre,))

            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de l'ajout du genre: {str(e)}")

    finally:
        con.close()

def update_genre(genre: Genre, data: Any) -> None:
    con = db.get_db_connection()

    try:
        if data.get("nomGenre"):
            genre.nom_genre = data["nomGenre"]

        with con.cursor() as cursor:
            cursor.execute(
                "UPDATE genre SET nomGenre = %s WHERE idGenre=%s",
                (genre.nom_genre, genre.id_genre)
            )
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la modification du genre: {str(e)}")

    finally:
        con.close()

def delete_genre(id_genre: int) -> None:
    con = db.get_db_connection()
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM genre WHERE idGenre=%s", (id_genre,))
            con.commit()
    except Exception as e:
        raise Exception(f"Erreur lors de la suppression du genre: {str(e)}")

    finally:
        con.close()
