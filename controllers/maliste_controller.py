from flask import Blueprint, jsonify, Response, request
import services.maliste_service as maliste_service
from models.maliste_model import MaListe

maliste_controller = Blueprint('maliste_controller', __name__, url_prefix='/maliste')

@maliste_controller.route("/", methods=["GET"])
def get_malistes() -> tuple[Response, int]:
    try:
        malistes = maliste_service.get_all_malistes()
        return jsonify([m.as_dict() for m in malistes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@maliste_controller.route("/<int:id_maliste>", methods=["GET"])
def get_maliste_by_id(id_maliste: int) -> tuple[Response, int]:
    try:
        maliste = maliste_service.get_maliste_by_id(id_maliste)
        if not maliste:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(maliste[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@maliste_controller.route("/", methods=["POST"])
def add_maliste() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["idProfil", "idTitre"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        maliste_service.create_maliste(MaListe.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@maliste_controller.route("/<int:id_maliste>", methods=["PUT"])
def update_maliste(id_maliste: int) -> tuple[Response, int]:
    try:
        maliste = maliste_service.get_maliste_by_id(id_maliste)
        if not maliste:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        maliste_service.update_maliste(maliste[0], data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@maliste_controller.route("/<int:id_maliste>", methods=["DELETE"])
def delete_maliste(id_maliste: int) -> tuple[Response, int]:
    try:
        maliste = maliste_service.get_maliste_by_id(id_maliste)
        if not maliste:
            return jsonify({"error": "Ressource inexistante"}), 404

        maliste_service.delete_maliste(id_maliste)
        return jsonify({"message": "Suppression de la liste effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500