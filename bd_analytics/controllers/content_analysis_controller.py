from flask import Blueprint, request, jsonify, Response
from datetime import datetime
from typing import Tuple, Optional, Any, Dict
from ..services.content_analysis_service import get_content_performance, get_top_content
from ..utils.format_response import format_response

content_analysis_controller = Blueprint('content_analysis', __name__, url_prefix='/content-analysis')


@content_analysis_controller.route('/performance', methods=['GET'])
def content_performance() -> Tuple[Response, int]:
    try:
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')
        time_range = None

        if date_debut and date_fin:
            time_range = (
                datetime.strptime(date_debut, '%Y-%m-%d'),
                datetime.strptime(date_fin, '%Y-%m-%d')
            )

        results = get_content_performance(time_range=time_range)

        return jsonify(format_response(
            success=True,
            data=results.to_dict(orient='records'),
            metadata={
                'date_range': {
                    'start': date_debut,
                    'end': date_fin
                } if date_debut and date_fin else None
            }
        )), 200

    except ValueError as e:
        return jsonify(format_response(
            success=False,
            error=f"Invalid date format: {str(e)}",
        )), 400

    except Exception as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
        )), 500


@content_analysis_controller.route('/top-content', methods=['GET'])
def top_content() -> Tuple[Response, int]:
    try:
        top_n = int(request.args.get('top_n', default=10))

        if top_n <= 0:
            raise ValueError("top_n must be a positive integer")

        results = get_top_content(top_n=top_n)

        return jsonify(format_response(
            success=True,
            data=results.to_dict(orient='records'),
            metadata={
                'top_n': top_n,
                'count': len(results)
            }
        )), 200

    except ValueError as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
        )), 400

    except Exception as e:
        return jsonify(format_response(
            success=False,
            error=str(e),
        )), 500