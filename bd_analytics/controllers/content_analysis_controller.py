from flask import Blueprint, request, jsonify
from bd_analytics.services.content_analysis_service import ContentAnalysisService
from datetime import datetime

content_analysis_blueprint = Blueprint('content_analysis', __name__, url_prefix='/content-analysis')


@content_analysis_blueprint.route('/performance', methods=['GET'])
def get_content_performance():
    """Analyse la performance des contenus"""
    try:
        # Paramètres
        metric = request.args.get('metric', default='views')
        content_type = request.args.get('content_type')

        # Gestion des dates
        date_debut = datetime.strptime(request.args['date_debut'], '%Y-%m-%d') if 'date_debut' in request.args else None
        date_fin = datetime.strptime(request.args['date_fin'], '%Y-%m-%d') if 'date_fin' in request.args else None

        # Appel du service
        service = ContentAnalysisService()
        results = service.get_content_performance(
            performance_metric=metric,
            time_range=(date_debut, date_fin) if date_debut and date_fin else None
        )

        return jsonify({
            'success': True,
            'data': results.to_dict(orient='records'),
            'metadata': {
                'metric': metric,
                'count': len(results)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@content_analysis_blueprint.route('/genre-comparison', methods=['GET'])
def compare_genres():
    """Compare les performances par genre"""
    try:
        service = ContentAnalysisService()
        results = service.analyze_genre_performance()
        return jsonify({
            'success': True,
            'data': results.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400