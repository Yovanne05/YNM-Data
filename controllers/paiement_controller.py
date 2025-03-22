from flask import Blueprint, jsonify, Response, request

import services.paiement_service as paiement_service
from models.paiement_model import Paiement

paiement_controller = Blueprint('paiement_controller', __name__, url_prefix='/paiement')

@paiement_controller.route("/", methods=["GET"])
def get_paiements() -> tuple[Response, int]:
    try:
        paiements = paiement_service.get_all_paiements()
        return jsonify([p.as_dict() for p in paiements]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@paiement_controller.route("/<int:id_paiement>", methods=["GET"])
def get_paiement_by_id(id_paiement: int) -> tuple[Response, int]:
    try:
        paiement = paiement_service.get_paiement_by_id(id_paiement)
        if not paiement:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify([p.as_dict() for p in paiement]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@paiement_controller.route("/", methods=["POST"])
def add_paiement() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["idUtilisateur", "idAbonnement", "idDate", "statusPaiement"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        paiement_service.create_paiement(Paiement.from_db_add(data))

        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@paiement_controller.route("/<int:id_paiement>", methods=["PUT"])
def update_paiement(id_paiement: int) -> tuple[Response, int]:
    try:
        paiement = paiement_service.get_paiement_by_id(id_paiement)
        if not paiement:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        paiement_service.update_paiement(paiement[0], data)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@paiement_controller.route("/<int:id_paiement>", methods=["DELETE"])
def delete_paiement(id_paiement: int) -> tuple[Response, int]:
    try:
        paiement = paiement_service.get_paiement_by_id(id_paiement)
        if not paiement:
            return jsonify({"error": "Ressource inexistante"}), 404

        paiement_service.delete_paiement(id_paiement)
        return jsonify({"message": "Suppression du paiement effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
