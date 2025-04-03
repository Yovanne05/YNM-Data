from flask_sqlalchemy import SQLAlchemy
from config import config

# Une seule instance SQLAlchemy pour toutes les bases
db = SQLAlchemy()


def init_app(app):
    """Initialise les connexions aux bases de données"""
    # Configuration principale
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri

    # Configuration des bases supplémentaires (binds)
    app.config['SQLALCHEMY_BINDS'] = {
        'entrepot': config.entrepot_db_uri
    }


    # Initialisation
    db.init_app(app)