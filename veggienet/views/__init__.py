from flask import Blueprint, redirect, render_template, session
from functools import wraps

views_bp = Blueprint('views', __name__)

def authenticated_view(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if session["authenticated"]:
                return f(*args, **kwargs)
        except:
            pass
        return redirect('/login?redirect=' + request.path)

    return decorated_function

@views_bp.route('/')
def index():
    return render_template('index.html')

from . import users
