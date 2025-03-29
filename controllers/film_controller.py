from flask import Blueprint, jsonify, Response, request
import services.film_service as film_service
from models.film_model import Film

film_controller = Blueprint('film_controller', __name__, url_prefix='/film')

@film_controller.route("/", methods=["GET"])
def get_films() -> tuple[Response, int]:
    try:
        films = film_service.get_all_films()
        return jsonify([f.as_dict() for f in films]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@film_controller.route("/<int:id_film>", methods=["GET"])
def get_film_by_id(id_film: int) -> tuple[Response, int]:
    try:
        film = film_service.get_film_by_id(id_film)
        if not film:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(film[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@film_controller.route("/", methods=["POST"])
def add_film() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["idTitre", "duree"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        film_service.create_film(Film.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@film_controller.route("/<int:id_film>", methods=["PUT"])
def update_film(id_film: int) -> tuple[Response, int]:
    try:
        film = film_service.get_film_by_id(id_film)
        if not film:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        film_service.update_film(film[0], data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@film_controller.route("/<int:id_film>", methods=["DELETE"])
def delete_film(id_film: int) -> tuple[Response, int]:
    try:
        film = film_service.get_film_by_id(id_film)
        if not film:
            return jsonify({"error": "Ressource inexistante"}), 404

        film_service.delete_film(id_film)
        return jsonify({"message": "Suppression du film effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500