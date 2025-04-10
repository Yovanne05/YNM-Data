from flask import Blueprint, jsonify
from bd_transactional.services.log_service import get_logs,clear_logs
log_controller = Blueprint('log_controller', __name__, url_prefix='/logs')

@log_controller.route("/", methods=["GET"])
def give_logs():
    try:
        logs = get_logs()
        return jsonify({"logs": logs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@log_controller.route("/", methods=["POST"])
def delete_logs():
    try:
        clear_logs()
        return jsonify({"message": "Logs effacés"}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500