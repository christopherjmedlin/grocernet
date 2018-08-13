from . import app, validators
from .models import User, save_to_database

from flask import session, g, request
from flask_restful import Resource, Api, abort, reqparse

import jwt
from werkzeug.security import check_password_hash

api = Api(app)

def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = g.get("authenticated", None)
        if authenticated:
            return f(*args, **kwargs)
        else if authenticated == None:
            try:
                payload = jwt.decode(session["jwt"], app.secret_key, algorithm='HS256')
                g.user = payload["user"]
                g.authenticated = True
            except Exception:
                abort(403, "Authentication is required for this endpoint")
        else:
            abort(403, "Authentication is required for this endpoint") 

def password(password):
    validators.validate_password(password)
    return password

def email(email):
    validators.validate_email(email)
    return email

def username(username):
    if ' ' in username:
        raise ValueError("Invalid username: cannot contain whitespace")
    return username
 
@api.resource('/users/<int:model_id>')
class UserResource(Resource): 
    def query_user(self, model_id):
        user = User.query.filter_by(id=model_id).first()
        if user != None:
            return user
        abort(404, message="Could not find user object with id: " + str(model_id))
    
    @property
    def user_parser(self):
        parser = RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=password, required=True)
        parser.add_argument("email", type=email, required=True)
        return parser

    def get(self, model_id):
        return self.query_user(model_id).to_dict()

    def post(self):
        args = self.user_parser.parse_args()
        save_to_database(User(args["username"], args["password"], args["email"], False))

@api.resource("/jwt/retrieve")
class LoginResource(Resource):
    def post():
        user = User.query.filter_by(username=request.data["username"])
        if not check_password_hash(request.data["password"]):
            abort(403, "Username or password is incorrect")
        token = jwt.encode({"user": request.data["username"], app.secret_key, algorithm="HS256")
