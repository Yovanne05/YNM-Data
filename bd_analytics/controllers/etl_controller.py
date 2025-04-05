from flask import Blueprint, jsonify, Response
from datetime import datetime
from typing import Tuple
from ..services.etl_service import extract_transform_load_all
from ..utils.format_response import format_response

etl_controller = Blueprint('etl', __name__, url_prefix='/etl')

@etl_controller.route('/run', methods=['POST'])
def run_etl() -> Tuple[Response, int]:
    """
    Exécuter le processus ETL complet
    """
    try:

        print("Démarrage du processus ETL")

        extract_transform_load_all()

        return jsonify(format_response(
            success=True,
            metadata={
                'timestamp': datetime.now().isoformat()
            }
        )), 200

    except Exception as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
            metadata={
                'timestamp': datetime.now().isoformat()
            }
        )), 500


@etl_controller.route('/status', methods=['GET'])
def etl_status() -> Tuple[Response, int]:
    """
    Vérifier le statut du dernier ETL
    """
    try:

        return jsonify(format_response(
            success=True,
            data={
                'last_execution': '2023-11-15T14:30:00',  # À remplacer
                'status': 'completed',
                'records_processed': 1250  # À remplacer
            }
        )), 200

    except Exception as e:
        return jsonify(format_response(
            success=False,
            error=str(e)
        )), 500