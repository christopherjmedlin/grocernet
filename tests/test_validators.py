import pytest

from veggienet.validators import validate_password, validate_email

@pytest.mark.parametrize("password", [
    ("!Lov3MyPiano"),
    ("SterlingGmail20.15"),
    ("BankLogin!3")
])
def test_validate_good_password(password):
    assert validate_password(password)

@pytest.mark.parametrize("password", [
    ("1234343211234"),
    ("short")
])
def test_validate_bad_password(password):
    err = None
    try:
        validate_password(password)
    except ValueError as e:
        err = e
    assert err != None

@pytest.mark.parametrize("email", [
    ("johndoe@gmail.com"),
    ("johndoe@yahoo.com")
])
def test_validate_good_email(email):
    assert validate_email(email)

@pytest.mark.parametrize("email", [
    ("What's an email?"),
    ("johndoe@gmailcom"),
    ("johndoegmail.com")
])
def test_validate_bad_email(email):
    err = None
    try:
        validate_email(email)
    except ValueError as e:
        err = e
    assert err != None

