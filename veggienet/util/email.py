from itsdangerous import URLSafeSerializer
from flask_mail import Mail, Message
from flask import current_app

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
