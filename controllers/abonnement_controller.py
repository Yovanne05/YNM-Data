from flask import Blueprint, jsonify, request, Response
from services.abonnement_service import get_all_abonnements, update_abonnement

abonnemment_controller = Blueprint('abonnemment_controller', __name__, url_prefix='/abonnement')

@abonnemment_controller.route("/", methods=["GET"])
def get_series() -> tuple[Response, int]:
    try:
        abonnements = get_all_abonnements()
        return jsonify([abonnement.as_dict() for abonnement in abonnements]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@abonnemment_controller.route("/", methods=["PUT"])
def update() -> tuple[Response, int]:
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        current_item = data.get('currentItem')
        updated_data = data.get('updatedData')

        if not all([current_item, updated_data]):
            return jsonify({"error": "Missing required fields"}), 400

        success = update_abonnement(current_item, updated_data)

        if success:
            return jsonify({
                "success": True,
                "message": "Abonnement mis à jour avec succès"
            }), 200
        else:
            return jsonify({"error": "Update failed"}), 500

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500