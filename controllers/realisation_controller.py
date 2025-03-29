from flask import Blueprint, jsonify, Response, request
import services.realisation_service as realisation_service
from models.realisation_model import Realisation

realisation_controller = Blueprint('realisation_controller', __name__, url_prefix='/realisation')

@realisation_controller.route("/", methods=["GET"])
def get_realisations() -> tuple[Response, int]:
    try:
        realisations = realisation_service.get_all_realisations()
        return jsonify([r.as_dict() for r in realisations]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@realisation_controller.route("/<int:id_realisation>", methods=["GET"])
def get_realisation_by_id(id_realisation: int) -> tuple[Response, int]:
    try:
        realisation = realisation_service.get_realisation_by_id(id_realisation)
        if not realisation:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(realisation[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@realisation_controller.route("/", methods=["POST"])
def add_realisation() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["idTitre", "idStudio"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        realisation_service.create_realisation(Realisation.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@realisation_controller.route("/<int:id_realisation>", methods=["DELETE"])
def delete_realisation(id_realisation: int) -> tuple[Response, int]:
    try:
        realisation = realisation_service.get_realisation_by_id(id_realisation)
        if not realisation:
            return jsonify({"error": "Ressource inexistante"}), 404

        realisation_service.delete_realisation(id_realisation)
        return jsonify({"message": "Suppression de la réalisation effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500