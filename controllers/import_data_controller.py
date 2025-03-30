from flask import Blueprint, jsonify, request, Response
import services.import_data_service as import_data_service

import_data_controller = Blueprint('import_data_controller', __name__, url_prefix='/import_data')

@import_data_controller.route('/', methods=['POST'])
def import_data():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier envoyé"}), 400
        import_data_service.save_file(request)
        table_name = request.form.get('tableName')
        import_data_service.import_data_to_db(table_name)
        return jsonify({"import": "Données de la table " + table_name + " ajoutées"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
