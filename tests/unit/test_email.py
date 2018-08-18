import pytest

from veggienet import email

def test_email_token():
    secret_key = "sdfjksfd;lasdf"
    token = email.generate_email_confirmation_token("user4321234@gmail.com", secret_key)
    assert token != "user4321234@gmail.com"

    email_address = email.confirm_email_confirmation_token(token, secret_key)
    assert email_address == "user4321234@gmail.com"

def test_invalid_token():
    token = "invalid token"

    result = email.confirm_email_confirmation_token(token, "asdf")
    assert not result
