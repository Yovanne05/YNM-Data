from flask import Blueprint, jsonify, request, Response
from services.abonnement_service import get_all_abonnements

abonnemment_controller = Blueprint('abonnemment_controller', __name__, url_prefix='/abonnement')

@abonnemment_controller.route("/", methods=["GET"])
def get_series() -> tuple[Response, int]:
    try:
        abonnements = get_all_abonnements()
        return jsonify([abonnement.as_dict() for abonnement in abonnements]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
