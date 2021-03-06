from flask import (Blueprint,
                   render_template,
                   request,
                   redirect,
                   session,
                   current_app,
                   url_for)
from .forms import (PasswordResetForm,
                    EmailForm,
                    SignUpForm,
                    AccountSettingsEmailForm,
                    AccountSettingsPasswordForm)
from .models import User
from grocernet.db import db, save_to_database
from grocernet.util.authentication import authenticated_view
from grocernet.util.email import (generate_email_confirmation_token,
                                  send_email,
                                  confirm_email_confirmation_token,
                                  send_activation_email,
                                  send_confirmation_email,
                                  censor_email)
from werkzeug.security import check_password_hash

users_views_bp = Blueprint('users_views', __name__)


@users_views_bp.route('/')
def index():
    return render_template('pages/users/index.html')


@users_views_bp.route('/login', methods=['GET', 'POST'])
def login():
    err = ""
    username = request.form.get("username", None)
    if username:
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password,
                                               request.form.get('password')):
            err = "Invalid username or password"
        else:
            if not user.activated:
                session["verification_email"] = censor_email(user.email)
                send_activation_email(user, current_app.secret_key)
                return redirect(url_for("users_views.verification_email_sent"))

            session["authenticated"] = True
            session["user"] = user.username
            session["email"] = user.email
            session["user_id"] = user.id

            return redirect(request.form.get('redirect'))

    redirect_url = request.args.get("redirect", "/")
    return render_template('pages/users/login.html',
                           redirect_url=redirect_url,
                           error=err)


@users_views_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@users_views_bp.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            form.errors["username"] = ["Username already taken"]
        else:
            user = User(form.username.data, form.password.data,
                        form.email.data, False)
            user.email_confirmed = False
            save_to_database(user)
            session["verification_email"] = censor_email(user.email)

            send_activation_email(user, current_app.secret_key)
            return redirect(url_for("users_views.verification_email_sent"))

    return render_template("pages/users/signup.html", form=form)


@users_views_bp.route('/email/verification-sent')
def verification_email_sent():
    return render_template("pages/users/verification-email-sent.html")


@users_views_bp.route('/email/verify/<token>')
def verify_email(token):
    email = None
    try:
        email = confirm_email_confirmation_token(token, current_app.secret_key)
    except Exception:
        return render_template("pages/users/verify-email.html",
                               invalid_token=True)

    user = User.query.filter_by(email=email).first()
    if user:
        user.email_confirmed = True
        user.activated = True
        db.session.commit()
    else:
        return render_template("pages/users/verify-email.html",
                               invalid_token=True)

    return render_template("pages/users/verify-email.html",
                           invalid_token=False)


@users_views_bp.route('/settings', methods=["GET", "POST"])
@authenticated_view
def user_settings():
    email_form = AccountSettingsEmailForm()
    password_form = AccountSettingsPasswordForm()
    confirmation_email_sent = False
    email_err = ""
    pass_err = ""
    email_success = False
    pass_success = False
    user = User.query.filter_by(username=session["user"]).first()

    if request.method == "POST":
        if email_form.change_email.data and \
           email_form.validate_on_submit():
            user.email = email_form.email.data
            user.email_confirmed = False
            send_confirmation_email(user, current_app.secret_key)
            confirmation_email_sent = True
            email_success = True
        if password_form.change_password.data and \
           password_form.validate_on_submit():
            user.set_password(password_form.password.data)
            pass_success = True
        db.session.commit()

        if email_form.errors:
            email_err = email_form.errors[next(iter(email_form.errors))][0]
        if password_form.errors:
            pass_err = password_form.errors[
                    next(iter(password_form.errors))
            ][0]

    return render_template("pages/users/user-settings.html",
                           email_form=email_form,
                           password_form=password_form,
                           confirmation_email_sent=confirmation_email_sent,
                           email_err=email_err,
                           pass_err=pass_err,
                           email_success=email_success,
                           pass_success=pass_success)


@users_views_bp.route('/password/reset', methods=["GET", "POST"])
def password_reset():
    form = EmailForm()

    if form.validate_on_submit():
        # check if there is actually a user associated with this email
        email = form.email.data
        if User.query.filter_by(email=email).first():
            token = generate_email_confirmation_token(email,
                                                      current_app.secret_key)
            reset_url = current_app.config["HOST"] + \
                url_for("users_views.password_reset_with_token", token=token)

            send_email("Reset Password", email,
                       render_template('email/password-reset.html',
                                       reset_url=reset_url))

            session["password_reset_email"] = censor_email(email)
        return redirect("/password/reset/email-sent")

    return render_template('pages/users/password-reset.html', form=form)


@users_views_bp.route('/password/reset/email-sent')
def password_reset_email_sent():
    if "password_reset_email" in session:
        return render_template('pages/users/password-reset-email-sent.html')
    return redirect(url_for("users_views.password_reset"))


@users_views_bp.route('/password/reset/<token>', methods=["GET", "POST"])
def password_reset_with_token(token):
    email = confirm_email_confirmation_token(token, current_app.secret_key)
    if not email:
        return redirect(url_for("users_views.password_reset"))
    user = User.query.filter_by(email=email).first()

    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for("users_views.password_reset_success"))

    return render_template('pages/users/password-reset-token.html',
                           form=form,
                           token=token,
                           username=user.username)


@users_views_bp.route('/password/success')
def password_reset_success():
    return render_template("pages/users/password-reset-success.html")
