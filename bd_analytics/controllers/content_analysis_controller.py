from flask import Blueprint, request, jsonify
from ..services.content_analysis_service import ContentAnalysisService
from datetime import datetime
from databases.db import db

content_analysis_blueprint = Blueprint('content_analysis', __name__, url_prefix='/content-analysis')


@content_analysis_blueprint.route('/performance', methods=['GET'])
def get_content_performance():
    try:
        metric = request.args.get('metric', default='views')
        date_debut = datetime.strptime(request.args['date_debut'], '%Y-%m-%d') if 'date_debut' in request.args else None
        date_fin = datetime.strptime(request.args['date_fin'], '%Y-%m-%d') if 'date_fin' in request.args else None

        service = ContentAnalysisService()
        results = service.get_content_performance(
            metric=metric,
            time_range=(date_debut, date_fin) if date_debut and date_fin else None
        )

        return jsonify({
            'success': True,
            'data': results.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400