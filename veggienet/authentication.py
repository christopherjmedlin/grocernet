import jwt
import datetime

from flask import g, session, request, current_app
from werkzeug.security import check_password_hash
from flask_restful import abort

# decorator for authenticated endpoints
def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            g.auth_token = auth_header.split(" ")[1]

        err_message = authenticate(g.get("auth_token", None))
        if err_message != '':
            abort(403, message=err_message)
        
        return f(*args, **kwargs)

def authenticate(token):
    payload = None
    try:
        payload = jwt.decode(token, current_app.secret_key, algorithm='HS256')
    except jwt.ExpiredSignatureError:
        g.authenticated = False
        return "Signature expired"
    except jwt.InvalidTokenError:
        g.authenticated = False
        return "Invalid token."
    g.user = payload["user"]
    g.authenticated = True
    return ''

def create_jwt(username, secret_key):
    """
    Creates a new JSON Web Token with an expiration time of 24 hours
    """
    token = jwt.encode({"user": username, 
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                        "iat": datetime.datetime.utcnow()}, 
                        secret_key, algorithm="HS256")
    return token.decode('utf-8')
    
# should be used inside flask_restful routes
def login(password_hash, password, username):
    if not check_password_hash(password_hash, password):
        return "Username or password is incorrect", 403
    token = create_jwt(username, current_app.secret_key)
    return {"jwt": token}, 202
