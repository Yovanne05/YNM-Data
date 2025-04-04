from flask import Blueprint, jsonify, Response
from typing import Dict, Any, Tuple
from ..services.comportement_analysis_service import get_daily_viewing_activity, get_viewing_analytics

behavior_analysis_blueprint = Blueprint('behavior_analysis', __name__, url_prefix='/behavior-analysis')

@behavior_analysis_blueprint.route('/engagement/<int:user_id>', methods=['GET'])
def user_engagement(user_id: int) -> Tuple[Response, int]:
    try:
        metrics = get_viewing_analytics(user_id=user_id)

        response_data: Dict[str, Any] = {
            'success': True,
            'data': metrics,
            'user_id': user_id
        }
        return jsonify(response_data), 200

    except Exception as e:
        error_response: Dict[str, Any] = {
            'success': False,
            'error': str(e)
        }
        return jsonify(error_response), 400


@behavior_analysis_blueprint.route('/viewing-activity', methods=['GET'])
def daily_viewing_activity() -> Tuple[Response, int]:
    try:
        patterns = get_daily_viewing_activity()

        response_data: Dict[str, Any] = {
            'success': True,
            'data': patterns
        }
        return jsonify(response_data), 200

    except Exception as e:
        error_response: Dict[str, Any] = {
            'success': False,
            'error': str(e)
        }
        return jsonify(error_response), 400