from . import app, validators
from .models import User, save_to_database

from flask_restful import Resource, Api, abort, reqparse

api = Api(app)

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


api.add_resource(UserResource, '/users/<int:model_id>')
