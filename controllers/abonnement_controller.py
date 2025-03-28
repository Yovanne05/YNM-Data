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


@abonnemment_controller.route("/<int:id_abonnement>", methods=["PUT"])
def update(id_abonnement: int) -> tuple[Response, int]:
    try:
        data = request.get_json()
        print("Received data:", data)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        success = update_abonnement(id_abonnement, data)

        if not success:
            print("Update failed - details:", {
                "id_abonnement": id_abonnement,
                "data": data,
                "success": success
            })
            return jsonify({"error": "Update failed", "details": "Check server logs"}), 500

        return jsonify({
            "success": True,
            "message": "Abonnement mis à jour avec succès",
            "updated": data
        }), 200

    except ValueError as e:
        print("Validation error:", str(e))
        return jsonify({"error": str(e), "type": "validation"}), 400
    except Exception as e:
        print("Server error:", str(e))
        return jsonify({"error": f"Internal error: {str(e)}", "type": "server"}), 500