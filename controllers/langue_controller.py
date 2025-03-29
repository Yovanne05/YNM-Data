from flask import Blueprint, jsonify, Response, request
import services.langue_service as langue_service
from models.langue_model import Langue

langue_controller = Blueprint('langue_controller', __name__, url_prefix='/langue')

@langue_controller.route("/", methods=["GET"])
def get_langues() -> tuple[Response, int]:
    try:
        langues = langue_service.get_all_langues()
        return jsonify([l.as_dict() for l in langues]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@langue_controller.route("/<int:id_langue>", methods=["GET"])
def get_langue_by_id(id_langue: int) -> tuple[Response, int]:
    try:
        langue = langue_service.get_langue_by_id(id_langue)
        if not langue:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(langue[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@langue_controller.route("/", methods=["POST"])
def add_langue() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if "nom" not in data:
            return jsonify({"error": "Le champ nom doit être fourni"}), 400

        langue_service.create_langue(Langue.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@langue_controller.route("/<int:id_langue>", methods=["PUT"])
def update_langue(id_langue: int) -> tuple[Response, int]:
    try:
        langue = langue_service.get_langue_by_id(id_langue)
        if not langue:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        langue_service.update_langue(langue[0], data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@langue_controller.route("/<int:id_langue>", methods=["DELETE"])
def delete_langue(id_langue: int) -> tuple[Response, int]:
    try:
        langue = langue_service.get_langue_by_id(id_langue)
        if not langue:
            return jsonify({"error": "Ressource inexistante"}), 404

        langue_service.delete_langue(id_langue)
        return jsonify({"message": "Suppression de la langue effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500