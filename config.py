from sqlalchemy.engine.url import URL

class Config:
    DB = {
        'drivername': 'mysql',
        'host': 'localhost',
        'username': 'root',
        'password': '',
        'database': 'netflixdb',
    }

    ENTREPOT = {
        'drivername': 'mysql',
        'host': 'localhost',
        'username': 'root',
        'password': '',
        'database': 'entrepot_netflix',
    }

    def get_db(self):
        return self.DB

    def get_entrepot(self):
        return self.ENTREPOT

    def get_db_url(self, config_name: str):
        config = getattr(self, config_name)
        return URL.create(**config)


config = Config()