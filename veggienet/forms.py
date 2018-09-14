from flask_wtf import FlaskForm
from wtforms import PasswordField, HiddenField, StringField
from wtforms.validators import EqualTo, InputRequired, Email, ValidationError
from .validators import validate_password

class PasswordResetForm(FlaskForm):
    token = HiddenField()
    password = PasswordField("New Password", [InputRequired(), EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")

    def validate_password(form, field):
        try:
            validate_password(field.data)
        except ValueError as e:
            raise ValidationError(str(e))

class PasswordResetEmailForm(FlaskForm):
    email = StringField("Email", [Email()])
