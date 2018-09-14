from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from veggienet.authentication import login
from veggienet.forms import PasswordResetForm, PasswordResetEmailForm
from veggienet.models import User, db
from veggienet.views import authenticated_view, views_bp
from veggienet.email import generate_email_confirmation_token, send_email, confirm_email_confirmation_token
from itsdangerous import URLSafeSerializer
from werkzeug.security import check_password_hash
from functools import wraps

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
            session["email"] = user.email
            return redirect(request.form.get('redirect'))
    
    redirect_url=request.args.get("redirect", "/")    
    return render_template('login.html', redirect_url=redirect_url, error=err)

@views_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@views_bp.route('/password/reset', methods=["GET", "POST"])
def password_reset():
    form = PasswordResetEmailForm()

    if form.validate_on_submit():
        # check if there is actually a user associated with this email
        email = form.email.data
        if User.query.filter_by(email=email).first():
            token = generate_email_confirmation_token(email, current_app.secret_key)
            reset_url = current_app.config["HOST"] + url_for("views.password_reset_with_token", token=token)

            send_email("Reset Password", email,
                    render_template('email/password-reset.html', reset_url=reset_url))
        
            session["password_reset_email"] = email
        return redirect("/password/reset/email-sent")

    if "email" in form.errors:
        err = form.errors["email"][0]
    return render_template('password-reset.html', form=form)

@views_bp.route('/password/reset/email-sent')
def password_reset_email_sent():
    return render_template('password-reset-email-sent.html')

@views_bp.route('/password/reset/<token>', methods=["GET", "POST"])
def password_reset_with_token(token):
    err = ""

    email = confirm_email_confirmation_token(token, current_app.secret_key)
    if not email:
        return redirect(url_for("views.password_reset"))
    user = User.query.filter_by(email=email).first()

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for("views.password_reset_success"))
   
    return render_template('password-reset-token.html', form=form, token=token, username=user.username)

@views_bp.route('/password/success')
def password_reset_success():
    return render_template("password-reset-success.html")
