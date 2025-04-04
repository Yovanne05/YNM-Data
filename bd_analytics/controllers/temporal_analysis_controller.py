from flask import Blueprint, request, jsonify, Response
from typing import Tuple, Dict, Any
from ..services.temporal_analysis_service import analyze_views_over_time

temporal_analysis_controller = Blueprint('temporal_analysis', __name__, url_prefix='/temporal-analysis')

@temporal_analysis_controller.route('/viewing-trends', methods=['GET'])
def get_viewing_trends() -> Tuple[Response, int]:
    try:
        period: str = request.args.get('period', default='year')
        if period not in {'day', 'month', 'year'}:
            raise ValueError("Le paramètre 'period' doit être 'day', 'month' ou 'year'")

        results = analyze_views_over_time(period=period)

        response_data: Dict[str, Any] = {
            'success': True,
            'data': results.to_dict(orient='records'),
            'period': period,
            'count': len(results)
        }
        return jsonify(response_data), 200

    except ValueError as e:
        error_data: Dict[str, Any] = {
            'success': False,
            'error': str(e),
            'allowed_periods': ['day', 'month', 'year']
        }
        return jsonify(error_data), 400

    except Exception as e:
        error_data: Dict[str, Any] = {
            'success': False,
            'error': 'Erreur interne du serveur' + str(e)
        }
        return jsonify(error_data), 500