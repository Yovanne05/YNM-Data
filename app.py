from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from controllers.utilisateur_controller import utilisateur_controller
import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

app.register_blueprint(utilisateur_controller)

@app.route('/tables', methods=['GET'])
def get_tables():
    conn = db.get_db_connection()
    try:
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
        cursor.close() 
