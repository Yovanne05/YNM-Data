from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from databases.db import db, init_app
from sqlalchemy import inspect

from controllers.transactional.abonnement_controller import abonnement_controller
from controllers.transactional.acteur_controller import acteur_controller
from controllers.transactional.acting_controller import acting_controller
from controllers.transactional.evaluation_controller import evaluation_controller
from controllers.transactional.film_controller import film_controller
from controllers.transactional.genre_controller import genre_controller
from controllers.transactional.import_data_controller import import_data_controller
from controllers.transactional.langue_controller import langue_controller
from controllers.transactional.languedispo_controller import languedisponible_controller
from controllers.transactional.maliste_controller import maliste_controller
from controllers.transactional.paiement_controller import paiement_controller
from controllers.transactional.profil_controller import profil_controller
from controllers.transactional.realisation_controller import realisation_controller
from controllers.transactional.serie_controller import serie_controller
from controllers.transactional.studio_controller import studio_controller
from controllers.transactional.titre_controller import titre_controller
from controllers.transactional.titregenre_controller import titregenre_controller
from controllers.transactional.utilisateur_controller import utilisateur_controller

blueprints = [
    abonnement_controller,
    acteur_controller,
    acting_controller,
    evaluation_controller,
    film_controller,
    genre_controller,
    import_data_controller,
    langue_controller,
    languedisponible_controller,
    maliste_controller,
    paiement_controller,
    profil_controller,
    realisation_controller,
    serie_controller,
    studio_controller,
    titre_controller,
    titregenre_controller,
    utilisateur_controller
]

app = Flask(__name__)
init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Max-Age", "86400")
        return response, 200


@app.route('/tables')
def get_tables():
    try:
        inspector = inspect(db.engine)
        tables_data = {}

        for table_name in inspector.get_table_names():
            columns = [column['name'] for column in inspector.get_columns(table_name)]
            tables_data[table_name] = columns

        return jsonify(tables_data)

    except Exception as e:
        app.logger.error(f"Error fetching tables: {str(e)}")
        return jsonify({"error": "Unable to fetch database structure"}), 500
@app.route('/test-db')
def test_db():
    try:
        with app.app_context():
            engine = db.get_engine()
            conn = engine.connect()
            conn.close()
            return jsonify({"status": "success", "message": "Connexion à la BDD réussie !"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500