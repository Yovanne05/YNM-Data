from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from controllers.utilisateur_controller import utilisateur_controller
from controllers.abonnement_controller import abonnemment_controller
import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

app.register_blueprint(utilisateur_controller)
app.register_blueprint(abonnemment_controller)

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

@app.route('/table/<table_name>', methods=['GET'])
def get_table_structure(table_name):
    conn = db.get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = [column['Field'] for column in cursor.fetchall()]

        return jsonify({table_name: columns})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()

@app.route('/table/<table_name>/data', methods=['GET'])
def get_table_data(table_name):
    conn = db.get_db_connection()
    try:
        filters = request.args.to_dict()

        with conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = [column['Field'] for column in cursor.fetchall()]

        query = f"SELECT * FROM `{table_name}`"
        params = []

        if filters:
            conditions = []
            for key, value in filters.items():
                if value and key in columns:
                    is_greater_than = filters.get(f"{key}_isGreaterThan") == "true"

                    if is_greater_than:
                        conditions.append(f"`{key}` > %s")
                    else:
                        conditions.append(f"`{key}` LIKE %s")
                    params.append(f"%{value}%" if not is_greater_than else value)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

        with conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            data = cursor.fetchall()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()