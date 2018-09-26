from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def save_to_database(model):
    db.session.add(model)
    db.session.commit()
