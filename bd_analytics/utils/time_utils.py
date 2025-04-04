from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import func

from databases.db import db

class TimeDimensionHelper:

    TIME_COLUMNS_MAPPING = {
        'day': ['jour', 'mois', 'annee'],
        'month': ['mois', 'annee'],
        'quarter': ['trimestre', 'annee'],
        'year': ['annee']
    }

    @classmethod
    def get_time_columns(cls, time_dimension):
        """Retourne les colonnes temporelles correspondantes"""
        return cls.TIME_COLUMNS_MAPPING.get(time_dimension, cls.TIME_COLUMNS_MAPPING['month'])

    @classmethod
    def get_time_column_expression(cls, period):
        """Retourne l'expression SQLAlchemy pour le regroupement temporel"""
        if period == 'monthly':
            return func.date_format(db.models['TempsDim'].idDate, '%Y-%m')
        elif period == 'quarterly':
            return func.concat(db.models['TempsDim'].annee, '-Q', db.models.TempsDim.trimestre)
        # Ajouter d'autres périodes au besoin
        return func.date_format(db.models['TempsDim'].idDate, '%Y-%m-%d')

    @classmethod
    def calculate_start_date(cls, period, last_n):
        """Calcule la date de début en fonction de la période"""
        end_date = datetime.now()
        if period == 'monthly':
            return end_date - relativedelta(months=last_n)
        elif period == 'quarterly':
            return end_date - relativedelta(months=last_n*3)
        # Ajouter d'autres périodes au besoin
        return end_date - relativedelta(days=last_n)