from veggienet.db import db
from werkzeug.security import generate_password_hash

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
    
    email_confirmed = db.Column(db.Boolean(), default=False, nullable=False)
    
    def __repr__(self):
        return '<User %r' % self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "admin": self.admin
        }
