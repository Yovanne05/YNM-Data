from flask import Blueprint, jsonify, request, Response
from services.utilisateur_service import get_all_utilisateurs

utilisateur_controller = Blueprint('utilisateur_controller', __name__, url_prefix='/utilisateur')

@utilisateur_controller.route("/", methods=["GET"])
def get_series() -> tuple[Response, int]:
    try:
        utilisateurs = get_all_utilisateurs()
        return jsonify([utilisateur.as_dict() for utilisateur in utilisateurs]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
