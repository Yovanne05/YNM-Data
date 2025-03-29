from flask import Blueprint, jsonify, Response, request
import services.profil_service as profil_service
from models.profil_model import Profil

profil_controller = Blueprint('profil_controller', __name__, url_prefix='/profil')

@profil_controller.route("/", methods=["GET"])
def get_profils() -> tuple[Response, int]:
    try:
        profils = profil_service.get_all_profils()
        return jsonify([p.as_dict() for p in profils]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profil_controller.route("/<int:id_profil>", methods=["GET"])
def get_profil_by_id(id_profil: int) -> tuple[Response, int]:
    try:
        profil = profil_service.get_profil_by_id(id_profil)
        if not profil:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify(profil[0].as_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profil_controller.route("/", methods=["POST"])
def add_profil() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["nom", "typeProfil", "idUtilisateur"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        profil_service.create_profil(Profil.from_db_add(data))
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profil_controller.route("/<int:id_profil>", methods=["PUT"])
def update_profil(id_profil: int) -> tuple[Response, int]:
    try:
        profil = profil_service.get_profil_by_id(id_profil)
        if not profil:
            return jsonify({"error": "Ressource inexistante"}), 404

        data = request.get_json()
        profil_service.update_profil(profil[0], data)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@profil_controller.route("/<int:id_profil>", methods=["DELETE"])
def delete_profil(id_profil: int) -> tuple[Response, int]:
    try:
        profil = profil_service.get_profil_by_id(id_profil)
        if not profil:
            return jsonify({"error": "Ressource inexistante"}), 404

        profil_service.delete_profil(id_profil)
        return jsonify({"message": "Suppression du profil effectuée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500