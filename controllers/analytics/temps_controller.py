from flask import Blueprint, jsonify
from services.analytics.temps_service import TempsService

test_controller = Blueprint("test", __name__, url_prefix="/test")


@test_controller.route('/', methods=['GET'])
def get_all_temps():
    try:
        temps_data = TempsService.get_all_as_dict()
        return jsonify(temps_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500