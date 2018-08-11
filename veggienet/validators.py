import re

def validate_password(password):
    validated = True
    err = "Invalid password: "
    if len(password) < 8:
        validated = False
        err += "Password should be over 8 characters long."
    if password.isdigit():
        validated = False
        err += "Password should not be entirely numeric."
    
    if not validated:
        raise ValueError(err)
    return True

def validate_email(email):
    if not re.match("^[^@]+@[^@]+\.[^@]+$", email):
        raise ValueError("Invalid email address.")
    return True
