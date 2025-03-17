from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import Config
from controllers.serie_controller import series_controller

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
mysql = MySQL(app)

app.register_blueprint(series_controller)

@app.route('/tables', methods=['GET'])
def get_tables():
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]

        result = {}
        for table in tables:
            cursor.execute("DESCRIBE `{}`".format(table))
            columns = [column[0] for column in cursor.fetchall()]
            result[table] = columns

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close() 
        
@app.route('/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    cursor = mysql.connection.cursor()
    try:
        query = "SELECT * FROM `{}`".format(table_name)
        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()