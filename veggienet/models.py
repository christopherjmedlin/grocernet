from flask import g
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash
import enum

db = SQLAlchemy()

class User(db.Model):
    def __init__(self, username, password, email, admin):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin

    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean())
    
    def __repr__(self):
        return '<User %r' % self.username

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "admin": self.admin
        }


class MeasurementUnit(enum.Enum):
    pound = "lb"
    basket = "basket"
    crop = "crop"

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000))

    measurement_unit = db.Column(db.Enum(MeasurementUnit), nullable=False)
    price_per_unit = db.Column(db.Integer, nullable=False)

    location = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return '<Listing %r>' % self.title


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(3000))

    def __repr__(self):
        return '<Message %r>' % self.subject

def save_to_database(model):
    db.session.add(model)
    db.session.commit()
