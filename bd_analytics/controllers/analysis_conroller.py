from flask import Blueprint, request, jsonify
from bd_analytics.services.cube_service import CubeService

analysis_controller = Blueprint('analysis', __name__, url_prefix='/analysis')


@analysis_controller.route('/connection', methods=['GET'])
def test_connection():
    """Route pour tester la connexion à la base de données"""
    try:
        is_connected = CubeService.test_connection()

        if is_connected:
            return jsonify({
                'status': 'success',
                'message': 'Connexion à la base de données établie avec succès'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'La connexion a réussi mais le test a échoué'
            }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Échec de la connexion: {str(e)}",
            'type': 'database_error'
        }), 500


@analysis_controller.route('/simple', methods=['GET'])
def test_simple():
    """Route pour tester une requête simple"""
    try:
        # Test plus simple et plus fiable
        with CubeService._get_session() as session:
            count = session.query(CubeService._get_model('TitreDim')).count()
            return jsonify({
                'status': 'success',
                'message': 'Requête simple exécutée',
                'count': count
            }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Échec de la requête test: {str(e)}",
            'type': 'database_error'
        }), 500


@analysis_controller.route('/top-content', methods=['GET'])
def get_top_content():
    """Route pour obtenir les contenus les plus populaires"""
    try:
        # Paramètres de requête
        limit = int(request.args.get('limit', 10))
        genre_id = request.args.get('genre_id', type=int)

        # Récupère les tops contenus
        top_content = CubeService.get_top_content(limit=limit, genre_id=genre_id)

        return jsonify({
            'status': 'success',
            'data': top_content
        }), 200
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'type': 'validation_error'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': "Une erreur technique est survenue",
            'type': 'server_error'
        }), 500


@analysis_controller.route('/visionnages', methods=['GET'])
def get_visionnages():
    """Route pour obtenir les statistiques de visionnage par période"""
    try:
        # Paramètres de période
        debut = request.args.get('debut', '2023-01-01')
        fin = request.args.get('fin', '2023-12-31')

        # Récupère les visionnages par période
        stats = CubeService.get_visionnages_par_periode(debut, fin)

        return jsonify({
            'status': 'success',
            'data': stats
        }), 200
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'type': 'validation_error'
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': "Une erreur technique est survenue",
            'type': 'server_error'
        }), 500