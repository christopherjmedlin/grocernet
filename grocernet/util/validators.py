import re


def validate_username(username):
    if ' ' in username:
        raise ValueError("Invalid username: cannot contain whitespace")
    if len(username) > 40:
        raise ValueError("Invalid username: must be less than 40 characters")
    return True


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
