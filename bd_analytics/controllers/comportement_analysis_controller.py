from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from typing import Tuple, Optional, Any, Dict
from ..services.comportement_analysis_service import get_daily_viewing_activity, get_viewing_analytics
from ..utils.format_response import format_response

behavior_analysis_controller = Blueprint('behavior_analysis', __name__, url_prefix='/behavior-analysis')

@behavior_analysis_controller.route('/engagement', methods=['GET'])
def global_engagement() -> Tuple[Response, int]:
    try:
        viewing_analysis = get_viewing_analytics()

        return jsonify(format_response(
            success=True,
            data=viewing_analysis
        )), 200

    except Exception as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
        )), 400

@behavior_analysis_controller.route('/viewing-activity', methods=['GET'])
def daily_viewing_activity() -> Tuple[Response, int]:
    try:
        activity = get_daily_viewing_activity()

        return jsonify(format_response(
            success=True,
            data=activity,
        )), 200

    except Exception as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
        )), 400
