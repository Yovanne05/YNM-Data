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