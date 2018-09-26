from itsdangerous import URLSafeSerializer
from flask_mail import Mail, Message
from flask import current_app, url_for, render_template

mail = Mail()


def generate_email_confirmation_token(email, secret_key):
    serializer = URLSafeSerializer(secret_key)
    return serializer.dumps(email)


def confirm_email_confirmation_token(token, secret_key):
    serializer = URLSafeSerializer(secret_key)
    try:
        email = serializer.loads(token)
    except Exception:
        return None
    return email


def send_email(subject, recipient, html):
    msg = Message(
        subject,
        recipients=[recipient],
        html=html,
    )
    mail.send(msg)


def send_activation_email(user, secret_key):
    token = generate_email_confirmation_token(user.email, secret_key)
    url = current_app.config["HOST"] + \
        url_for("users_views.verify_email", token=token)
    email_html = render_template(
        "email/activation-email.html",
        confirm_url=url)
    send_email("Activate Your Veggienet Account", user.email, email_html)


def send_confirmation_email(user, secret_key):
    token = generate_email_confirmation_token(user.email, secret_key)
    url = current_app.config["HOST"] + \
        url_for("users_views.verify_email", token=token)
    email_html = render_template(
        "email/confirmation-email.html",
        confirm_url=url)
    send_email("Confirm Your Veggienet Email", user.email, email_html)


def censor_email(email):
    censored = ""
    for index, character in enumerate(email):
        if index > 0 and index < email.rfind("@"):
            censored += "*"
        else:
            censored += character
    return censored
