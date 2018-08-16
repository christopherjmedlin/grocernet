from veggienet import validators
from veggienet.models import User, save_to_database, db

from flask import session, g, request, current_app, Blueprint
from flask_restful import Resource, Api, abort, reqparse

import jwt
from werkzeug.security import check_password_hash

users_bp = Blueprint('users', __name__, url_prefix='/users')
api = Api(users_bp)

def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = g.get("authenticated", None)
        if authenticated:
            return f(*args, **kwargs)
        elif authenticated == None:
            try:
                payload = jwt.decode(session["jwt"], current_app.secret_key, algorithm='HS256')
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
 
user_parser = RequestParser()
user_parser.add_argument("username", type=str, required=True)
user_parser.add_argument("password", type=password, required=True)
user_parser.add_argument("email", type=email, required=True)

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
        args = user_parser.parse_args()
        if args["password"]:
            abort(400, message="Password must be changed using password reset endpoint")
        user = User.query.filter_by(id=model_id)
        user.username = args["username"]
        user.email = args["email"]
        return '', 201

@api.resource("/jwt/retrieve")
class LoginResource(Resource):
    def post():
        user = User.query.filter_by(username=request.data["username"])
        if not check_password_hash(request.data["password"]):
            abort(403, "Username or password is incorrect")
        token = jwt.encode({"user": request.data["username"]}, current_app.secret_key, algorithm="HS256")
        return {"jwt": token}, 202
