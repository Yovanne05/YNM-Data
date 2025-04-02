import pymysql
from config import Config

pymysql.install_as_MySQLdb()

def get_db_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB_ENTREPOT,
        cursorclass=pymysql.cursors.DictCursor
    )
