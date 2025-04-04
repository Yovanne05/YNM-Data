# databases/database_session.py
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from .db import db


@contextmanager
def get_db_session():
    engine = db.get_engine(bind='entrepot')
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