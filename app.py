from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config

from controllers.abonnement_controller import abonnement_controller
from controllers.acteur_controller import acteur_controller
from controllers.acting_controller import acting_controller
from controllers.evaluation_controller import evaluation_controller
from controllers.film_controller import film_controller
from controllers.genre_controller import genre_controller
from controllers.import_data_controller import import_data_controller
from controllers.langue_controller import langue_controller
from controllers.languedispo_controller import languedisponible_controller
from controllers.maliste_controller import maliste_controller
from controllers.paiement_controller import paiement_controller
from controllers.profil_controller import profil_controller
from controllers.realisation_controller import realisation_controller
from controllers.serie_controller import serie_controller
from controllers.studio_controller import studio_controller
from controllers.temps_controller import temps_controller
from controllers.titre_controller import titre_controller
from controllers.titregenre_controller import titregenre_controller
from controllers.utilisateur_controller import utilisateur_controller

import db
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

app.register_blueprint(abonnement_controller)
app.register_blueprint(acteur_controller)
app.register_blueprint(acting_controller)
app.register_blueprint(evaluation_controller)
app.register_blueprint(film_controller)
app.register_blueprint(genre_controller)
app.register_blueprint(import_data_controller)
app.register_blueprint(langue_controller)
app.register_blueprint(languedisponible_controller)
app.register_blueprint(maliste_controller)
app.register_blueprint(paiement_controller)
app.register_blueprint(profil_controller)
app.register_blueprint(realisation_controller)
app.register_blueprint(serie_controller)
app.register_blueprint(studio_controller)
app.register_blueprint(temps_controller)
app.register_blueprint(titre_controller)
app.register_blueprint(titregenre_controller)
app.register_blueprint(utilisateur_controller)

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Max-Age", "86400")
        return response, 200
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