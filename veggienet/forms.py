from flask_wtf import FlaskForm
from wtforms import PasswordField, HiddenField, StringField
from wtforms.validators import EqualTo, InputRequired, Email

class PasswordResetForm(FlaskForm):
    token = HiddenField()
    password = PasswordField("New Password", [InputRequired(), EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")

class PasswordResetEmailForm(FlaskForm):
    email = StringField("Email", [Email()])
