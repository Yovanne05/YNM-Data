from flask import Blueprint, request, jsonify
from bd_analytics.services.temporal_analysis_service import TemporalAnalysisService
from datetime import datetime, timedelta
from databases.db import db

temporal_analysis_blueprint = Blueprint('temporal_analysis', __name__, url_prefix='/temporal-analysis')


@temporal_analysis_blueprint.route('/time-series', methods=['GET'])
def get_time_series():
    """Analyse des séries temporelles"""
    try:
        # Paramètres
        metric = request.args.get('metric', default='views')
        period = request.args.get('period', default='monthly')
        last_n = int(request.args.get('last_n', default=12))

        # Appel du service
        service = TemporalAnalysisService()
        results = service.get_time_series_analysis(
            metric=metric,
            period=period,
            last_n=last_n
        )

        return jsonify({
            'success': True,
            'data': results.to_dict(orient='records'),
            'analysis_period': f"Last {last_n} {period}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@temporal_analysis_blueprint.route('/period-comparison', methods=['GET'])
def compare_periods():
    """Compare deux périodes temporelles avec valeurs par défaut"""
    try:
        metric = request.args.get('metric', 'views')

        default_end = datetime.now()
        default_start_p1 = default_end - timedelta(days=30)
        default_start_p2 = default_start_p1 - timedelta(days=30)

        period1_start = datetime.strptime(request.args.get('period1_start', default_start_p1.strftime('%Y-%m-%d')),
                                          '%Y-%m-%d')
        period1_end = datetime.strptime(request.args.get('period1_end', default_end.strftime('%Y-%m-%d')), '%Y-%m-%d')
        period2_start = datetime.strptime(request.args.get('period2_start', default_start_p2.strftime('%Y-%m-%d')),
                                          '%Y-%m-%d')
        period2_end = datetime.strptime(request.args.get('period2_end', default_start_p1.strftime('%Y-%m-%d')),
                                        '%Y-%m-%d')

        if period1_start >= period1_end:
            raise ValueError("period1_start doit être avant period1_end")
        if period2_start >= period2_end:
            raise ValueError("period2_start doit être avant period2_end")

        service = TemporalAnalysisService()
        comparison = service.compare_periods(
            metric=metric,
            period1=(period1_start, period1_end),
            period2=(period2_start, period2_end)
        )

        return jsonify({
            'success': True,
            'data': comparison,
            'parameters': {
                'metric': metric,
                'period1': {
                    'start': period1_start.strftime('%Y-%m-%d'),
                    'end': period1_end.strftime('%Y-%m-%d')
                },
                'period2': {
                    'start': period2_start.strftime('%Y-%m-%d'),
                    'end': period2_end.strftime('%Y-%m-%d')
                },
                'note': "Les dates étaient optionnelles - valeurs par défaut utilisées"
            }
        })

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "Erreur de validation des paramètres",
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e),
            'message': "Erreur interne du serveur"
        }), 500