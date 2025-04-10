from sqlalchemy import text

from databases.db import db

def reset_db():
    db.drop_all()
    db.create_all()

def add_sample_data():
    with open("script/netflix_transactional_insert.sql", "r", encoding="utf-8") as file:
        fichier_insert = file.read()

    with db.engine.connect() as connexion:
        with connexion.begin():
            for ligne in fichier_insert.split(";"):
                insert = ligne.strip()
                if insert:
                    connexion.execute(text(insert))