from flask import Blueprint, jsonify, Response, request

import services.titre_service as titre_service
from models.titre_model import Titre

titre_controller = Blueprint('titre_controller', __name__, url_prefix='/titre')

@titre_controller.route("/", methods=["GET"])
def get_titres() -> tuple[Response, int]:
    try:
        titres = titre_service.get_all_titres()
        return jsonify([titres.as_dict() for titres in titres]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@titre_controller.route("/<int:id_titre>", methods=["GET"])
def get_titre_by_id(id_titre: int) -> tuple[Response, int]:
    try:
        titre = titre_service.get_titre_by_id(id_titre)
        if not titre:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify([titre.as_dict() for titre in titre]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@titre_controller.route("/", methods=["POST"])
def add_titre() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if not all(champ in data for champ in ["nom", "annee", "iddateDebutLicence","iddateFinLicence", "idGenre", "categorieAge", "description"]):
            return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

        titre_service.create_titre(Titre.from_db_add(data))

        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@titre_controller.route("/<int:id_titre>", methods=["PUT"])
def update_titre(id_titre: int) -> tuple[Response, int]:
    try:
        titre = titre_service.get_titre_by_id(id_titre)
        if titre:
            data = request.get_json()
            titre_service.update_titre(titre[0], data)
            return jsonify(data), 200
        else:
            return jsonify({"error": "Ressource inexistante"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@titre_controller.route("/<int:id_titre>", methods=["DELETE"])
def delete_titre(id_titre: int) -> tuple[Response, int]:
    try:
        titre = titre_service.get_titre_by_id(id_titre)
        if titre:
            titre_service.delete_titre(id_titre)
            return jsonify({"message": "Suppression du titre effectuée"}), 200
        else:
            return jsonify({"error": "Ressource inexistante"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500