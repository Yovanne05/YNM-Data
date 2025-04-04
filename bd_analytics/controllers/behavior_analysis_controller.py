from flask import Blueprint, request, jsonify
from datetime import datetime
from functools import wraps
from bd_analytics.services.comportement_analysis_service import ComportementAnalysisService


behavior_analysis_blueprint = Blueprint('behavior_analysis', __name__,
                                        url_prefix='/behavior-analysis')



# Validateur de paramètres
def validate_params(params):
    """Valide les paramètres de requête"""
    errors = {}

    # Validation de la dimension temporelle
    time_dimension = params.get('time_dimension', 'month')
    if time_dimension not in ['day', 'month', 'quarter', 'year']:
        errors['time_dimension'] = "Doit être l'un de: day, month, quarter, year"

    # Validation du segment utilisateur
    user_segment = params.get('user_segment')
    if user_segment and user_segment not in ['age_group', 'country', 'subscription_type']:
        errors['user_segment'] = "Segment utilisateur non valide"

    # Validation des dates
    date_range = {}
    for date_param in ['date_debut', 'date_fin']:
        if date_param in params:
            try:
                date_range[date_param] = datetime.strptime(params[date_param], '%Y-%m-%d')
            except ValueError:
                errors[date_param] = "Format de date invalide (YYYY-MM-DD attendu)"

    if errors:
        raise ValueError(jsonify({
            'success': False,
            'errors': errors,
            'message': "Paramètres de requête invalides"
        }))

    return {
        'time_dimension': time_dimension,
        'user_segment': user_segment,
        'date_range': (date_range.get('date_debut'), date_range.get('date_fin'))
        if 'date_debut' in date_range and 'date_fin' in date_range else None
    }


@behavior_analysis_blueprint.route('/viewing-patterns', methods=['GET'])
def get_viewing_patterns():
    """
    Analyse des motifs de visionnage
    ---
    tags:
      - Comportement
    parameters:
      - name: time_dimension
        in: query
        type: string
        enum: [day, month, quarter, year]
        default: month
      - name: user_segment
        in: query
        type: string
        enum: [age_group, country, subscription_type]
      - name: date_debut
        in: query
        type: string
        format: date
      - name: date_fin
        in: query
        type: string
        format: date
      - name: content_type
        in: query
        type: string
      - name: genres
        in: query
        type: array
        items:
          type: string
    responses:
      200:
        description: Données d'analyse du comportements
      400:
        description: Paramètres invalides
      500:
        description: Erreur serveur
    """
    # Validation des paramètres
    validated = validate_params(request.args)

    # Construction des filtres
    content_filter = {
        'content_type': request.args.get('content_type'),
        'genres': request.args.getlist('genres'),
        'date_range': validated['date_range']
    }

    # Appel du service
    service = ComportementAnalysisService()
    results = service.get_viewing_behavior(
        time_dimension=validated['time_dimension'],
        content_filter=content_filter
    )

    # Formatage de la réponse
    response_data = {
        'success': True,
        'data': results.to_dict(orient='records'),
        'metadata': {
            'time_dimension': validated['time_dimension'],
            'user_segment': validated['user_segment'] or 'none',
            'date_range': {
                'debut': validated['date_range'][0].isoformat() if validated['date_range'] else None,
                'fin': validated['date_range'][1].isoformat() if validated['date_range'] else None
            },
            'record_count': len(results)
        }
    }

    return jsonify(response_data)


@behavior_analysis_blueprint.route('/engagement-metrics/<int:user_id>', methods=['GET'])
def get_engagement_metrics(user_id):
    """
    Métriques d'engagement utilisateur
    ---
    tags:
      - Comportement
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Métriques d'engagement
      400:
        description: ID utilisateur invalide
      500:
        description: Erreur serveur
    """
    if user_id <= 0:
        raise ValueError("L'ID utilisateur doit être un nombre positif")

    service = ComportementAnalysisService()
    metrics = service.analyze_engagement_metrics(user_id=user_id)

    return jsonify({
        'success': True,
        'data': metrics,
        'user_id': user_id
    })