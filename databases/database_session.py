# databases/database_session.py
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from .db import db

@contextmanager
def get_db_session(bind=None):
    """
    Context manager pour obtenir une session SQLAlchemy.

    Args:
        bind (str, optional): Nom du bind de base de données à utiliser.
                             Si None, utilise la base de données principale.
    """
    engine = db.get_engine(bind=bind)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        session.close()

@contextmanager
def get_main_db_session():
    """Context manager pour obtenir une session de la base de données principale."""
    with get_db_session(bind=None) as session:
        yield session

@contextmanager
def get_db_entrepot_session():
    """Context manager pour obtenir une session de la base de données entrepot."""
    with get_db_session(bind='entrepot') as session:
        yield session