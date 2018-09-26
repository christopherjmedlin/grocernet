from flask import session
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Email, ValidationError
from .models import User
from grocernet.util.validators import validate_password, validate_username
from werkzeug.security import check_password_hash


def username_validator(form, field):
    try:
        validate_username(field.data)
    except ValueError as e:
        raise ValidationError(str(e))


def password_validator(form, field):
    try:
        validate_password(field.data)
    except ValueError as e:
        raise ValidationError(str(e))


def current_password_validator(form, field):
    if "user" in session:
        user = User.query.filter_by(username=session["user"]).first()
        if not check_password_hash(user.password, field.data):
            raise ValidationError("Current password is invalid.")
    else:
        raise ValidationError("Your session is invalidated. Please log in.")


class SignUpForm(FlaskForm):
    username = StringField("Username", [username_validator])
    password = PasswordField("Password",
                             [InputRequired(),
                              password_validator,
                              EqualTo("confirm",
                                      message="Passwords must match")])
    confirm = PasswordField("Confirm Password")
    email = StringField("Email", [Email()])


class PasswordResetForm(FlaskForm):
    password = PasswordField("Password",
                             [InputRequired(),
                              password_validator,
                              EqualTo("confirm",
                                      message="Passwords must match")])

    confirm = PasswordField("Confirm Password")


class EmailForm(FlaskForm):
    email = StringField("Email", [Email()])


class AccountSettingsEmailForm(FlaskForm):
    current_password = PasswordField("Current Password",
                                     [current_password_validator])
    email = StringField("Email", [Email()])

    # submit field exists here to differentiate between
    # different forms on the same page, same for password form
    change_email = SubmitField("Change Email")


class AccountSettingsPasswordForm(FlaskForm):
    current_password = PasswordField("Current Password",
                                     [current_password_validator])
    password = PasswordField("Password",
                             [InputRequired(),
                              password_validator,
                              EqualTo("confirm",
                                      message="Passwords must match")])
    confirm = PasswordField("Confirm Password")
    change_password = SubmitField("Change Password")
