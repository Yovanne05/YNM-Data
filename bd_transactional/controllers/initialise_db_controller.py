from flask import Blueprint, jsonify, request

from bd_transactional.services import initialise_db_service

initialise_db_controller = Blueprint('initialise_db_controller', __name__, url_prefix='/initialise')

@initialise_db_controller.route('/', methods=['POST'])
def reset_db():
    try:
        initialise_db_service.reset_db()
        return jsonify({"initialisation": "Base de données réinitialisée"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500