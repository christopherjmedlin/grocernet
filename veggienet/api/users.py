from veggienet import validators
from veggienet.models import User, save_to_database, db
from veggienet.authentication import login, authentication_required

from flask import session, g, request, current_app, Blueprint
from flask_restful import Resource, Api, abort, reqparse
from copy import deepcopy

from werkzeug.security import check_password_hash

users_bp = Blueprint('users', __name__, url_prefix='/users')
api = Api(users_bp)

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
 
user_edit_parser = reqparse.RequestParser()
user_edit_parser.add_argument("username", type=str, required=True)
user_edit_parser.add_argument("email", type=email, required=True)

user_create_parser = deepcopy(user_edit_parser)
user_create_parser.add_argument("password", type=password, required=True)

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
        args = user_edit_parser.parse_args()
        user = User.query.filter_by(id=model_id).first()
        user.username = args["username"]
        user.email = args["email"]
        db.session.commit()
        return '', 201

login_parser = reqparse.RequestParser()
login_parser.add_argument("username", type=str, required=True)
login_parser.add_argument("password", type=str, required=True)

@api.resource("/jwt/retrieve")
class LoginResource(Resource):
    def post():
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args["username"])
        return login(user.password, args["password"]), 202
