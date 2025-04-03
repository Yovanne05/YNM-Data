from sqlalchemy.engine.url import URL
from typing import Dict, Any


class Config:
    DB_COMMON = {
        'drivername': 'mysql+pymysql',
        'host': 'localhost',
        'username': 'root',
        'password': '',
        'query': {'charset': 'utf8mb4'}
    }

    DATABASES = {
        'transactional': {
            **DB_COMMON,
            'database': 'netflixdb'
        },
        'entrepot': {
            **DB_COMMON,
            'database': 'entrepot_netflix'
        }
    }

    def get_db_config(self, db_type: str) -> Dict[str, Any]:
        """Récupère la configuration pour un type de base spécifique"""
        if db_type not in self.DATABASES:
            raise ValueError(f"Type de base inconnu: {db_type}. Options: {list(self.DATABASES.keys())}")
        return self.DATABASES[db_type]

    def get_db_url(self, db_type: str) -> str:
        """Génère l'URL de connexion sous forme de string"""
        config = self.get_db_config(db_type)
        url = f"mysql+pymysql://{config['username']}@{config['host']}/{config['database']}"
        if 'port' in config:
            url = f"mysql+pymysql://{config['username']}@{config['host']}:{config['port']}/{config['database']}"
        return url

    @property
    def db_uri(self) -> str:
        return self.get_db_url('transactional')

    @property
    def entrepot_db_uri(self) -> str:
        return self.get_db_url('entrepot')


config = Config()