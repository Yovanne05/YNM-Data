from datetime import datetime, timedelta
from operator import and_

from bd_analytics.models.dimensions.temps_model import TempsDim
from bd_analytics.models.facts.visionnage_model import VisionnageFact


class ETLService:
    def __init__(self, db_session):
        self.db = db_session

    def load_date_dimension(self, start_date, end_date):
        """Charge la dimension Temps"""
        current_date = start_date
        while current_date <= end_date:
            date_record = TempsDim(
                jour=current_date.day,
                mois=current_date.month,
                annee=current_date.year,
                trimestre=(current_date.month - 1) // 3 + 1,
                jour_semaine=current_date.weekday(),
                est_weekend=current_date.weekday() >= 5
            )
            self.db.add(date_record)
            current_date += timedelta(days=1)
        self.db.commit()

    def transform_and_load(self, raw_data, data_type):
        #TODO : A CONTINUER POUR TOUTES LES TABLES
        """Transforme et charge les données dans l'entrepôt"""
        if data_type == 'visionnage':
            self._process_visionnage_data(raw_data)
        elif data_type == 'utilisateur':
            self._process_user_data(raw_data)
        # Ajouter d'autres types au besoin

    def _process_visionnage_data(self, raw_data):
        """Traitement des données de visionnage"""
        for record in raw_data:
            visionnage = VisionnageFact(
                idUtilisateur=record['user_id'],
                idTitre=record['content_id'],
                idDate=self._get_date_id(record['view_date']),
                dureeVisionnage=record['duration'],
                nombreVues=record['views']
            )
            self.db.add(visionnage)
        self.db.commit()

    def _get_date_id(self, date_str):
        """Convertit une date en ID de dimension Temps"""
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        result = self.db.query(TempsDim.idDate).filter(
            and_(
                TempsDim.jour == date_obj.day,
                TempsDim.mois == date_obj.month,
                TempsDim.annee == date_obj.year
            )
        ).first()
        return result[0] if result else None