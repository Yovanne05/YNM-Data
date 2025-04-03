from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    app.config['SQLALCHEMY_BINDS'] = {
        'entrepot': config.entrepot_db_uri
    }

    db.init_app(app)
    with app.app_context():
        db.create_all()