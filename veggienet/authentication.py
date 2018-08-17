import jwt

from flask import g, session, request, current_app
from werkzeug.security import check_password_hash
from flask_restful import abort

# decorator for authenticated endpoints
def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = g.get("authenticated", None)
        if authenticated:
            return f(*args, **kwargs)
        elif authenticated == None or authenticate(session["jwt"]):
            pass
        else:
            abort(403, message="Authentication is required for this endpoint")

def authenticate(token):
    payload = None
    try:
        payload = jwt.decode(token, current_app.secret_key, algorithm='HS256')
    except Exception:
        return False
    g.user = payload["user"]
    g.authenticated = True
    return payload

# should be used inside flask_restful routes
def login(password_hash, password, username):
    if not check_password_hash(password_hash, password):
        return "Username or password is incorrect", 403
    token = jwt.encode({"user": username}, current_app.secret_key, algorithm="HS256")
    return token, 202
