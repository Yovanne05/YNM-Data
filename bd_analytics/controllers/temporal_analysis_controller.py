from flask import Blueprint, request, jsonify, Response
from typing import Tuple, Dict, Any
from ..services.temporal_analysis_service import analyze_views_over_time
from ..utils.format_response import format_response
temporal_analysis_controller = Blueprint('temporal_analysis', __name__, url_prefix='/temporal-analysis')

@temporal_analysis_controller.route('/viewing-trends', methods=['GET'])
def get_viewing_trends() -> Tuple[Response, int]:
    try:
        period = request.args.get('period', default='year')

        if period not in {'day', 'month', 'year'}:
            raise ValueError("Period must be 'day', 'month' or 'year'")

        results = analyze_views_over_time(period=period)

        return jsonify(format_response(
            success=True,
            data=results.to_dict(orient='records'),
            metadata={
                'period': period,
                'count': len(results)
            }
        )), 200

    except ValueError as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
            metadata={
                'allowed_periods': ['day', 'month', 'year']
            }
        )), 400

    except Exception as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
        )), 500