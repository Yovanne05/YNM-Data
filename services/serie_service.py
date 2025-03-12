from db import mysql
from models.serie_model import Serie
import MySQLdb

def get_all_series():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Serie")
        result = cursor.fetchall()
        series = [Serie.from_db(row) for row in result]
        cursor.close()
        return series
    except Exception as e:
        raise Exception(f"Error fetching series: {str(e)}")
    
def get_series_by_genre(genre: str):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Serie WHERE genre=%s", (genre,))
        result = cursor.fetchall()
        series = [Serie.from_db(row) for row in result]
        cursor.close()
        return series
    except Exception as e:
        raise Exception(f"Error fetching series by genre: {str(e)}")
    
def get_series_by_year(year: int):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Serie WHERE annee=%s", (year,))
        result = cursor.fetchall()
        series = [Serie.from_db(row) for row in result]
        cursor.close()
        return series
    except Exception as e:
        raise Exception(f"Error fetching series by year: {str(e)}")
    
def create(nom: str, genre: str, saison: int, annee: int, dateDebutLicence: str, dateFinLicence: str, categorieAge: str, description: str):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO Serie (nom, genre, saison, annee, dateDebutLicence, dateFinLicence, categorieAge, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, genre, saison, annee, dateDebutLicence, dateFinLicence, categorieAge, description))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        raise Exception(f"Error inserting Serie: {str(e)}")

def update(idSerie: int, nom: str = None, genre: str = None, saison: int = None, annee: int = None, 
           dateDebutLicence: str = None, dateFinLicence: str = None, categorieAge: str = None, description: str = None):
    try:
        cursor = mysql.connection.cursor()
        query = "UPDATE Serie SET"
        params = []

        if nom is not None:
            query += " nom=%s,"
            params.append(nom)
        if genre is not None:
            query += " genre=%s,"
            params.append(genre)
        if saison is not None:
            query += " saison=%s,"
            params.append(saison)
        if annee is not None:
            query += " annee=%s,"
            params.append(annee)
        if dateDebutLicence is not None:
            query += " dateDebutLicence=%s,"
            params.append(dateDebutLicence)
        if dateFinLicence is not None:
            query += " dateFinLicence=%s,"
            params.append(dateFinLicence)
        if categorieAge is not None:
            query += " categorieAge=%s,"
            params.append(categorieAge)
        if description is not None:
            query += " description=%s,"
            params.append(description)

        query = query.rstrip(',') + " WHERE idSerie=%s"
        params.append(idSerie)

        cursor.execute(query, tuple(params))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        raise Exception(f"Error updating Serie: {str(e)}")


def delete(idSerie: int):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM Serie WHERE idSerie=%s", (idSerie,))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        raise Exception(f"Error deleting Serie: {str(e)}")

def get_by_id(idSerie: int):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Serie WHERE idSerie=%s", (idSerie,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return Serie.from_db(result)
        else:
            return None
    except Exception as e:
        raise Exception(f"Error fetching Serie by ID: {str(e)}")