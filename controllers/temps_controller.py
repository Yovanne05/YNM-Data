from flask import Blueprint, jsonify, Response, request

import services.temps_service as temps_service
from models.temps_model import Temps

temps_controller = Blueprint('temps_controller', __name__, url_prefix='/temps')

@temps_controller.route("/", methods=["GET"])
def get_temps() -> tuple[Response, int]:
    try:
        temps = temps_service.get_all_temps()
        return jsonify([t.as_dict() for t in temps]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@temps_controller.route("/<int:id_date>", methods=["GET"])
def get_temps_by_id(id_date: int) -> tuple[Response, int]:
    try:
        temps = temps_service.get_temps_by_id(id_date)
        if not temps:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify([t.as_dict() for t in temps]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@temps_controller.route("/", methods=["POST"])
def add_temps() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["jour", "mois", "annee", "trimestre"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        temps_service.create_temps(Temps.from_db_add(data))

        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@temps_controller.route("/<int:id_date>", methods=["PUT"])
def update_temps(id_date: int) -> tuple[Response, int]:
    try:
        temps = temps_service.get_temps_by_id(id_date)
        if temps:
            data = request.get_json()
            temps_service.update_temps(temps[0], data)
            return jsonify(data), 200
        else:
            return jsonify({"error": "Ressource inexistante"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@temps_controller.route("/<int:id_date>", methods=["DELETE"])
def delete_temps(id_date: int) -> tuple[Response, int]:
    try:
        temps = temps_service.get_temps_by_id(id_date)
        if temps:
            temps_service.delete_temps(id_date)
            return jsonify({"message": "Suppression de la date effectuée"}), 200
        else:
            return jsonify({"error": "Ressource inexistante"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
