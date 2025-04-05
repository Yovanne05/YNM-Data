from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from typing import Tuple, Optional, Any, Dict
from ..services.content_analysis_service import get_content_performance, get_top_content

content_analysis_controller = Blueprint('content_analysis', __name__, url_prefix='/content-analysis')


@content_analysis_controller.route('/performance', methods=['GET'])
def content_performance() -> Tuple[Response, int]:
    try:
        date_debut: Optional[str] = request.args.get('date_debut')
        date_fin: Optional[str] = request.args.get('date_fin')

        time_range: Optional[Tuple[datetime, datetime]] = None
        if date_debut and date_fin:
            time_range = (
                datetime.strptime(date_debut, '%Y-%m-%d'),
                datetime.strptime(date_fin, '%Y-%m-%d')
            )

        results = get_content_performance(time_range=time_range)

        response_data: Dict[str, Any] = {
            'success': True,
            'data': results.to_dict(orient='records')
        }
        return jsonify(response_data), 200

    except ValueError as e:

        error_data: Dict[str, Any] = {
            'success': False,
            'error': f"Format de date invalide : {str(e)}"
        }
        return jsonify(error_data), 400
    except Exception as e:

        error_data: Dict[str, Any] = {
            'success': False,
            'error': str(e)
        }
        return jsonify(error_data), 400


@content_analysis_controller.route('/top-content', methods=['GET'])
def top_content() -> Tuple[Response, int]:
    try:
        top_n: int = int(request.args.get('top_n', default=10))

        if top_n <= 0:
            raise ValueError("top_n doit être un entier positif")

        results = get_top_content(top_n=top_n)

        response_data: Dict[str, Any] = {
            'success': True,
            'data': results.to_dict(orient='records'),
            'params': {'top_n': top_n}
        }
        return jsonify(response_data), 200

    except ValueError as e:
        error_data: Dict[str, Any] = {
            'success': False,
            'error': str(e)
        }
        return jsonify(error_data), 400

    except Exception as e:
        error_data: Dict[str, Any] = {
            'success': False,
            'error': "Erreur interne du serveur" + str(e)
        }
        return jsonify(error_data), 500