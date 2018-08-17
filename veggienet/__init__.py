from flask import Flask
from .api.users import users_bp
from .models import db
from flask_migrate import Migrate

def create_app(config_path='../instance/config.py', testing=False):
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(users_bp)

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['TEST_DATABASE_URI']

    db.init_app(app)
    migrate = Migrate(app, db)

    return app
