from veggienet.util import validators
from .models import User
from veggienet.db import save_to_database, db
from veggienet.util.authentication import login, authentication_required, create_jwt
from veggienet.util.email import generate_email_confirmation_token, confirm_email_confirmation_token, send_email

from flask import session, g, request, current_app, Blueprint, render_template
from flask_restful import Resource, Api, abort, reqparse

from werkzeug.security import check_password_hash

users_api_bp = Blueprint('users_api', __name__, url_prefix='/api/v1/users')
api = Api(users_api_bp)

def password(password):
    validators.validate_password(password)
    return password

def email(email):
    validators.validate_email(email)
    return email

def username(username):
    validators.validate_username(username)
    return username

def get_user_edit_parser():
    user_edit_parser = reqparse.RequestParser()
    user_edit_parser.add_argument("username", type=username, required=True)
    user_edit_parser.add_argument("email", type=email, required=True)
    return user_edit_parser

def get_login_parser():
    login_parser = reqparse.RequestParser()
    login_parser.add_argument("username", type=str, required=True)
    login_parser.add_argument("password", type=str, required=True)
    return login_parser

@api.resource('/<int:model_id>')
class UserResource(Resource): 
    def query_user(self, model_id):
        user = User.query.filter_by(id=model_id).first()
        if user != None:
            return user
        abort(404, message="Could not find user object with id: " + str(model_id))
    
    def get(self, model_id):
        return self.query_user(model_id).to_dict()

    def put(self, model_id):
        args = get_user_edit_parser().parse_args()
        user = User.query.filter_by(id=model_id).first()
        user.username = args["username"]
        user.email = args["email"]
        db.session.commit()
        return '', 201

@api.resource("/jwt/retrieve")
class LoginResource(Resource):
    def post(self):
        """
        If username and password is valid, returns a JWT containing the username,
        intended to be used for authentication in the Authentication HTTP header.
        """
        args = get_login_parser().parse_args()
        user = User.query.filter_by(username=args["username"]).first()
        return login(user.password, args["password"], args["username"])

@api.resource("/jwt/refresh")
class JWTRefreshResource(Resource):
    method_decorators = [authentication_required]

    def get(self):
        """
        Refreshes the expiration time for the JSON web token.

        JWT still needs to be valid in order for this to work, if the JWT
        expires the user needs to login again.
        """
        return {"jwt": create_jwt(g.get("user"), current_app.secret_key)}
