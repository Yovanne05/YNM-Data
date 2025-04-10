from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from databases.db import db, init_app
from sqlalchemy import inspect
from config import config

from sqlalchemy import text
from bd_transactional.controllers.abonnement_controller import abonnement_controller
from bd_transactional.controllers.acteur_controller import acteur_controller
from bd_transactional.controllers.acting_controller import acting_controller
from bd_transactional.controllers.evaluation_controller import evaluation_controller
from bd_transactional.controllers.film_controller import film_controller
from bd_transactional.controllers.genre_controller import genre_controller
from bd_transactional.controllers.import_data_controller import import_data_controller
from bd_transactional.controllers.langue_controller import langue_controller
from bd_transactional.controllers.languedispo_controller import languedisponible_controller
from bd_transactional.controllers.maliste_controller import maliste_controller
from bd_transactional.controllers.paiement_controller import paiement_controller
from bd_transactional.controllers.profil_controller import profil_controller
from bd_transactional.controllers.realisation_controller import realisation_controller
from bd_transactional.controllers.serie_controller import serie_controller
from bd_transactional.controllers.studio_controller import studio_controller
from bd_transactional.controllers.titre_controller import titre_controller
from bd_transactional.controllers.titregenre_controller import titregenre_controller
from bd_transactional.controllers.utilisateur_controller import utilisateur_controller

from bd_analytics.controllers.content_analysis_controller import content_analysis_controller
from bd_analytics.controllers.comportement_analysis_controller import behavior_analysis_controller
from bd_analytics.controllers.temporal_analysis_controller import temporal_analysis_controller
from bd_analytics.controllers.etl_controller import etl_controller
from bd_transactional.controllers.initialise_db_controller import initialise_db_controller

blueprints = [
    etl_controller,
    content_analysis_controller,
    behavior_analysis_controller,
    abonnement_controller,
    temporal_analysis_controller,
    acteur_controller,
    acting_controller,
    evaluation_controller,
    film_controller,
    genre_controller,
    import_data_controller,
    initialise_db_controller,
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
    utilisateur_controller,
]

app = Flask(__name__)
app.config.from_object(config)
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
        __bind_key__ = 'transactional'
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

@app.route('/check-db')
def check_db():
    try:
        engine = db.get_engine(app, bind='entrepot')
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM Temps"))
            count = result.scalar()
            return f"La table Temps contient {count} enregistrements"
    except Exception as e:
        return f"Erreur: {str(e)}", 500