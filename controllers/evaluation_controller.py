from flask import Blueprint, jsonify, Response, request
import services.evaluation_service as evaluation_service
from models.evaluation_model import Evaluation

evaluation_controller = Blueprint('evaluation_controller', __name__, url_prefix='/evaluation')

@evaluation_controller.route("/", methods=["GET"])
def get_evaluations() -> tuple[Response, int]:
    try:
        evaluations = evaluation_service.get_all_evaluations()
        return jsonify([e.as_dict() for e in evaluations]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@evaluation_controller.route("/<int:id_evaluation>", methods=["GET"])
def get_evaluation_by_id(id_evaluation: int) -> tuple[Response, int]:
    try:
        evaluation = evaluation_service.get_evaluation_by_id(id_evaluation)
        if not evaluation:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(evaluation[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@evaluation_controller.route("/", methods=["POST"])
def add_evaluation() -> tuple[Response, int]:
    try:
        data = request.get_json()
        required_fields = ["idProfil", "idTitre", "note"]
        if not all(champ in data for champ in required_fields):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        evaluation_service.create_evaluation(Evaluation.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@evaluation_controller.route("/<int:id_evaluation>", methods=["PUT"])
def update_evaluation(id_evaluation: int) -> tuple[Response, int]:
    try:
        evaluation = evaluation_service.get_evaluation_by_id(id_evaluation)
        if not evaluation:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        evaluation_service.update_evaluation(evaluation[0], data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@evaluation_controller.route("/<int:id_evaluation>", methods=["DELETE"])
def delete_evaluation(id_evaluation: int) -> tuple[Response, int]:
    try:
        evaluation = evaluation_service.get_evaluation_by_id(id_evaluation)
        if not evaluation:
            return jsonify({"error": "Ressource inexistante"}), 404

        evaluation_service.delete_evaluation(id_evaluation)
        return jsonify({"message": "Suppression de l'évaluation effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500