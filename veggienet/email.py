from itsdangerous import URLSafeSerializer

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
