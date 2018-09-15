from flask import Flask
from .users.api import users_api_bp
from .users.views import users_views_bp
from .db import db
from .email import mail
from flask_migrate import Migrate

def create_app(config_path='../instance/config.py', testing=False):
    app = Flask(__name__, static_folder="static/dist")
    app.config.from_pyfile('../instance/config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = testing

    app.register_blueprint(users_api_bp)
    app.register_blueprint(users_views_bp)

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['TEST_DATABASE_URI']

    db.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)

    return app
