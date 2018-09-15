from flask import g
from flask_sqlalchemy import SQLAlchemy

import enum

db = SQLAlchemy()

def save_to_database(model):
    db.session.add(model)
    db.session.commit()
