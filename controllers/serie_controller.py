from flask import Blueprint, jsonify, Response, request
import services.serie_service as serie_service
from models.serie_model import Serie

serie_controller = Blueprint('serie_controller', __name__, url_prefix='/serie')

@serie_controller.route("/", methods=["GET"])
def get_series() -> tuple[Response, int]:
    try:
        series = serie_service.get_all_series()
        return jsonify([s.as_dict() for s in series]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@serie_controller.route("/<int:id_serie>", methods=["GET"])
def get_serie_by_id(id_serie: int) -> tuple[Response, int]:
    try:
        serie = serie_service.get_serie_by_id(id_serie)
        if not serie:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(serie[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@serie_controller.route("/", methods=["POST"])
def add_serie() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["idTitre", "saison"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        serie_service.create_serie(Serie.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@serie_controller.route("/<int:id_serie>", methods=["PUT"])
def update_serie(id_serie: int) -> tuple[Response, int]:
    try:
        serie = serie_service.get_serie_by_id(id_serie)
        if not serie:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        serie_service.update_serie(serie[0], data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@serie_controller.route("/<int:id_serie>", methods=["DELETE"])
def delete_serie(id_serie: int) -> tuple[Response, int]:
    try:
        serie = serie_service.get_serie_by_id(id_serie)
        if not serie:
            return jsonify({"error": "Ressource inexistante"}), 404

        serie_service.delete_serie(id_serie)
        return jsonify({"message": "Suppression de la série effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500