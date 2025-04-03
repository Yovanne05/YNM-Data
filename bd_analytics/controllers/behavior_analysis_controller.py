from flask import Blueprint, request, jsonify
from bd_analytics.services.behavior_analysis_service import BehaviorAnalysisService
from datetime import datetime

behavior_analysis_blueprint = Blueprint('behavior_analysis', __name__, url_prefix='/behavior-analysis')


@behavior_analysis_blueprint.route('/viewing-patterns', methods=['GET'])
def get_viewing_patterns():
    """Analyse des motifs de visionnage par dimensions"""
    try:
        time_dimension = request.args.get('time_dimension', default='month')
        if time_dimension not in ['day', 'month', 'quarter', 'year']:
            raise ValueError("Dimension temporelle invalide")

        user_segment = request.args.get('user_segment')
        if user_segment and user_segment not in ['age_group', 'country', 'subscription_type']:
            raise ValueError("Segment utilisateur invalide")

        date_debut = None
        date_fin = None
        if 'date_debut' in request.args:
            try:
                date_debut = datetime.strptime(request.args['date_debut'], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Format de date début invalide (YYYY-MM-DD attendu)")

        if 'date_fin' in request.args:
            try:
                date_fin = datetime.strptime(request.args['date_fin'], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Format de date fin invalide (YYYY-MM-DD attendu)")

        filters = {
            'content_type': request.args.get('content_type'),
            'genres': request.args.getlist('genres'),
            'date_range': (date_debut, date_fin) if date_debut and date_fin else None
        }

        service = BehaviorAnalysisService()

        results = service.get_viewing_behavior(
            time_dimension=time_dimension,
            user_segment=user_segment,
            content_filter=filters
        )

        return jsonify({
            'success': True,
            'data': results.to_dict(orient='records'),
            'metadata': {
                'time_dimension': time_dimension,
                'user_segment': user_segment,
                'date_range': f"{date_debut.date() if date_debut else 'N/A'} to {date_fin.date() if date_fin else 'N/A'}"
            }
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "Erreur de validation des paramètres"
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "Erreur interne du serveur"
        }), 500


@behavior_analysis_blueprint.route('/engagement-metrics/<int:user_id>', methods=['GET'])
def get_engagement_metrics(user_id):
    """Récupère les métriques d'engagement pour un utilisateur"""
    try:
        service = BehaviorAnalysisService()
        metrics = service.analyze_engagement_metrics(user_id=user_id)

        return jsonify({
            'success': True,
            'data': metrics,
            'user_id': user_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f"Impossible de récupérer les métriques pour l'utilisateur {user_id}"
        }), 400