from veggienet import create_app
from veggienet.authentication import authenticate, login
from flask import g
import jwt
from werkzeug.security import generate_password_hash

app = create_app(testing=True)

def test_authenticate():
    token = jwt.encode({"user": "user12345"}, app.secret_key, algorithm="HS256")
    with app.app_context():
        with app.test_request_context():
            authenticate(token)
            assert g.get("authenticated", None) == True
            assert g.get("user", None) == "user12345"

def test_invalid_authenticate():
    token = "badtoken"
    with app.app_context():
        with app.test_request_context():
            result = authenticate(token)
            assert result != ''
            assert g.get("authenticated") == False
            assert g.get("user", None) == None

def test_login():
    result = None
    with app.app_context():
        result = login(generate_password_hash("W0!fP@ck"), "W0!fP@ck", "user1124")
    token = result[0]
    payload = jwt.decode(token["jwt"], app.secret_key, algorithm='HS256')

    assert payload["user"] == "user1124"
    assert result[1] == 202

def test_invalid_login():
    result = None
    with app.app_context():
        result = login(generate_password_hash("W0!fP@ck"), "invalid", "user1124")
    
    assert result == ("Username or password is incorrect", 403)

