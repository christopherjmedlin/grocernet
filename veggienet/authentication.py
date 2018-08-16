import jwt

from flask import g, session, request
from werkzeug.security import check_password_hash
from flask_restful import abort

# decorator for authenticated endpoints
def authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = g.get("authenticated", None)
        if authenticated:
            return f(*args, **kwargs)
        elif authenticated == None:
            authenticate(session["jwt"])
        else:
            abort(403, "Authentication is required for this endpoint")

def authenticate(jwt):
    try:
        payload = jwt.decode(session["jwt"], current_app.secret_key, algorithm='HS256')
        g.user = payload["user"]
        g.authenticated = True
    except Exception:
        abort(403, "Authentication is required for this endpoint")

# should be used inside flask_restful routes
def login(password_hash, password):
    if not check_password_hash(password_hash, password):
        abort(403, "Username or password is incorrect")
    return jwt.encode({"user": request.data["username"]}, current_app.secret_key, algorithm="HS256")
