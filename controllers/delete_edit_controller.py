from flask import Blueprint, request, jsonify
from services.delete_edit_service import Delete_Edit_Services

# Créer un Blueprint pour les routes de suppression et modification
delete_edit_controller = Blueprint('delete_edit_controller', __name__, url_prefix='/delete_edit')

# Route pour supprimer un élément
@delete_edit_controller.route('/<table_name>/<int:item_id>', methods=['DELETE'])
def delete_item(table_name, item_id):
    print(table_name, item_id)
    try:
        result = Delete_Edit_Services.delete_item(table_name, item_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour modifier un élément
@delete_edit_controller.route('/<table_name>/<int:item_id>', methods=['PUT'])
def update_item(table_name, item_id):
    try:
        data = request.get_json()
        result = Delete_Edit_Services.update_item(table_name, item_id, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500