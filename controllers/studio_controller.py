from flask import Blueprint, jsonify, Response, request
import services.studio_service as studio_service
from models.studio_model import Studio

studio_controller = Blueprint('studio_controller', __name__, url_prefix='/studio')

@studio_controller.route("/", methods=["GET"])
def get_studios() -> tuple[Response, int]:
    try:
        studios = studio_service.get_all_studios()
        return jsonify([s.as_dict() for s in studios]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@studio_controller.route("/<int:id_studio>", methods=["GET"])
def get_studio_by_id(id_studio: int) -> tuple[Response, int]:
    try:
        studio = studio_service.get_studio_by_id(id_studio)
        if not studio:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(studio[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@studio_controller.route("/", methods=["POST"])
def add_studio() -> tuple[Response, int]:
    try:
        data = request.get_json()
        required_fields = ["nom", "pays"]
        if not all(champ in data for champ in required_fields):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        studio_service.create_studio(Studio.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@studio_controller.route("/<int:id_studio>", methods=["PUT"])
def update_studio(id_studio: int) -> tuple[Response, int]:
    try:
        studio = studio_service.get_studio_by_id(id_studio)
        if not studio:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        studio_service.update_studio(studio[0], data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@studio_controller.route("/<int:id_studio>", methods=["DELETE"])
def delete_studio(id_studio: int) -> tuple[Response, int]:
    try:
        studio = studio_service.get_studio_by_id(id_studio)
        if not studio:
            return jsonify({"error": "Ressource inexistante"}), 404

        studio_service.delete_studio(id_studio)
        return jsonify({"message": "Suppression du studio effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500