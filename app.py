from flask import Flask, jsonify
import pymysql
from flask_cors import CORS
from config import Config
from controllers.serie_controller import series_controller

pymysql.install_as_MySQLdb()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

def get_db_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

app.register_blueprint(series_controller)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/tables', methods=['GET'])
def get_tables():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [table['Tables_in_' + Config.MYSQL_DB] for table in cursor.fetchall()]

        result = {}
        for table in tables:
            with conn.cursor() as cursor:
                cursor.execute(f"DESCRIBE `{table}`")
                columns = [column['Field'] for column in cursor.fetchall()]
                result[table] = columns

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

