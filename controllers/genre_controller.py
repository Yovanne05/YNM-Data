from flask import Blueprint, jsonify, Response, request

import services.genre_service as genre_service
from models.genre_model import Genre

genre_controller = Blueprint('genre_controller', __name__, url_prefix='/genre')

@genre_controller.route("/", methods=["GET"])
def get_genres() -> tuple[Response, int]:
    try:
        genres = genre_service.get_all_genres()
        return jsonify([genre.as_dict() for genre in genres]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genre_controller.route("/<int:id_genre>", methods=["GET"])
def get_genre_by_id(id_genre: int) -> tuple[Response, int]:
    try:
        genre = genre_service.get_genre_by_id(id_genre)
        if not genre:
            return jsonify({"error": "Ressource inexistante"}), 404
        return jsonify([genre.as_dict() for genre in genre]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genre_controller.route("/", methods=["POST"])
def add_genre() -> tuple[Response, int]:
    try:
        data = request.get_json()
        if "nomGenre" not in data:
            return jsonify({"error": "Le champ 'nomGenre' est requis"}), 400

        genre_service.create_genre(Genre.from_db_add(data))

        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genre_controller.route("/<int:id_genre>", methods=["PUT"])
def update_genre(id_genre: int) -> tuple[Response, int]:
    try:
        genre = genre_service.get_genre_by_id(id_genre)
        if genre:
            data = request.get_json()
            genre_service.update_genre(genre[0], data)
            return jsonify(data), 200
        else:
            return jsonify({"error": "Ressource inexistante"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@genre_controller.route("/<int:id_genre>", methods=["DELETE"])
def delete_genre(id_genre: int) -> tuple[Response, int]:
    try:
        genre = genre_service.get_genre_by_id(id_genre)
        if genre:
            genre_service.delete_genre(id_genre)
            return jsonify({"message": "Suppression du genre effectuée"}), 200
        else:
            return jsonify({"error": "Ressource inexistante"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500