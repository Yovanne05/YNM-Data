from sqlalchemy.engine.url import URL

class Config:
    DB = {
        'drivername': 'mysql',
        'host': 'localhost',
        'username': 'root',
        'password': '',
        'database': 'netflixdb',
    }

    @property
    def current_db(self):
        return self.DB

    def get_db_url(self, config_name='current_db'):
        config = getattr(self, config_name)
        return URL.create(**config)


config = Config()