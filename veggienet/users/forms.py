from flask_wtf import FlaskForm
from wtforms import PasswordField, HiddenField, StringField
from wtforms.validators import EqualTo, InputRequired, Email, ValidationError
from veggienet.util.validators import validate_password, validate_username

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

class SignUpForm(FlaskForm):
    username = StringField("Username", [username_validator])
    password = PasswordField("Password", [InputRequired(), password_validator, EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")
    email = StringField("Email", [Email()])

class PasswordResetForm(FlaskForm):
    token = HiddenField()
    password = PasswordField("New Password", [InputRequired(), password_validator, EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")

class PasswordResetEmailForm(FlaskForm):
    email = StringField("Email", [Email()])
