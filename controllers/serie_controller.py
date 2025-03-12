from flask import Blueprint, jsonify, request, Response
from services.serie_service import get_all_series, get_series_by_genre, get_series_by_year, create, update, delete, get_by_id

series_controller = Blueprint('serie_controller', __name__, url_prefix='/series')

@series_controller.route("/", methods=["GET"])
def get_series() -> tuple[Response, int]:
    try:
        series = get_all_series()
        return jsonify([serie.as_dict() for serie in series]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@series_controller.route("/<string:genre>", methods=["GET"])
def get_series_by_genre_route(genre: str) -> tuple[Response, int]:
    try:
        series = get_series_by_genre(genre)
        return jsonify([serie.as_dict() for serie in series]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@series_controller.route("/<int:year>", methods=["GET"])
def get_series_by_year_route(year: int) -> tuple[Response, int]:
    try:
        series = get_series_by_year(year)
        return jsonify([serie.as_dict() for serie in series]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@series_controller.route("/", methods=["POST"])
def create_series() -> tuple[Response, int]:
    try:
        data = request.get_json()
        champ_requis = ["nom", "genre", "saison", "annee", "dateDebutLicence", "dateFinLicence", "categorieAge", "description"]
        
        for champ in champ_requis:
            if champ not in data:
                return jsonify({"error": f"Missing required field: {champ}"}), 400
        
        create(data["nom"], data["genre"], data["saison"], data["annee"], data["dateDebutLicence"], 
               data["dateFinLicence"], data["categorieAge"], data["description"])
        return jsonify({"message": "Serie created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@series_controller.route("/<int:idSerie>", methods=["PUT"])
def update_series(idSerie: int) -> tuple[Response, int]:
    try:
        data = request.get_json()
        update(idSerie, **data)
        return jsonify({"message": "Serie updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@series_controller.route("/<int:idSerie>", methods=["DELETE"])
def delete_series(idSerie: int) -> tuple[Response, int]:
    try:
        delete(idSerie)
        return jsonify({"message": "Serie deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@series_controller.route("/<int:idSerie>", methods=["GET"])
def get_series_by_id(idSerie: int) -> tuple[Response, int]:
    try:
        serie = get_by_id(idSerie)
        if serie:
            return jsonify(serie.as_dict()), 200
        else:
            return jsonify({"error": "Serie not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
