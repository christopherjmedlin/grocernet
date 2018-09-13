from flask import Blueprint, render_template, request, redirect, session
from veggienet.authentication import login
from veggienet.models import User
from werkzeug.security import check_password_hash

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    err = ""
    if request.form.get('username', None):
        user = User.query.filter_by(username=request.form.get('username')).first()
        if not user or not check_password_hash(user.password, request.form.get('password')):
            err = "Invalid username or password"
        else:
            session["authenticated"] = True
            session["user"] = user.username
            return redirect(request.form.get('redirect'))
    
    redirect_url=request.args.get("redirect", "/")    
    return render_template('login.html', redirect_url=redirect_url, error=err)

@views_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')
