import pytest
import json
import jwt
import datetime

from veggienet import create_app
from veggienet import models
from veggienet.email import mail

from werkzeug.security import check_password_hash
from itsdangerous import URLSafeSerializer
from flask import g

app = create_app(testing=True)

TEST_PASSWORD = "!Lov3MyPiano"

def query_user(user_id):
    """
    Helper for querying user from database with proper app context
    """
    with app.app_context():
        return models.User.query.filter_by(id=user_id).first()

def query_user_by_username(username):
    with app.app_context():
        return models.User.query.filter_by(username=username).first()

def post_user(client):
    response = client.post('/users/', data={"username": "user24315",
                        "email": "user24315@gmail.com", "password": "s3cur3P@$$w0rd"})
    return response

@pytest.fixture(scope="module")
def client():
    return app.test_client()

@pytest.fixture(scope="function")
def db():
    with app.app_context():
        models.db.drop_all()
        models.db.create_all()
        return models.db

@pytest.fixture(scope="function")
def user():
    user = models.User("user234134", "!Lov3MyPiano",
                       "user234134@gmail.com", False)
    with app.app_context():
        models.save_to_database(user)
        # re-query user so it isn't expired and SQLAlchemy doesn't
        # attempt to refresh attributes
        return query_user(user.id)

def test_user_retrieve(client, db, user):
    response = client.get('/users/' + str(user.id))
    data = response.data.decode('utf-8')
    
    assert user.username in data
    assert user.password not in data
    assert TEST_PASSWORD not in data

def test_user_put(client, db, user):
    response = client.put('/users/' + str(user.id),
            data={"username": "user23413", "email": "user234134@gmail.com"})
    user = query_user(user.id)

    assert user.username == 'user23413'
    assert user.email == 'user234134@gmail.com'
        
def test_valid_user_post(client, db):
    response = None


    with mail.record_messages() as outbox:
        response = post_user(client)
        assert len(outbox) == 1
        assert app.config["FRONTEND_HOST"] in outbox[0].html

    user = query_user_by_username("user24315")

    assert user.password != "s3cur3P@$$w0rd"
    assert user.email == "user24315@gmail.com"
    assert check_password_hash(user.password, "s3cur3P@$$w0rd")
    assert not user.admin

@pytest.mark.parametrize("username,password,email", [
    (None, None, None),
    ("user34737", "278374", "user34737@gmail.com"),
    ("Mr. Smith", "s3cur3P@$$w0rd", "mrsmith@gmail.com"),
    ("user73758", "s3cur3P@$$w0rd", "user73758@gmailcom")
])
def test_invalid_user_post(client, db, username, password, email):
    response = client.post('/users/', data={"username": username,
                        "email": email, "password": password})
        
    assert response.status_code == 400
    assert b"Invalid" in response.data or b"Missing" in response.data

def test_login(client, db, user):
    response = client.post('/users/jwt/retrieve', data={"username": user.username,
                                                            "password": TEST_PASSWORD})
    token = json.loads(response.data.decode('utf-8'))["jwt"].encode('utf-8')

    assert response.status_code == 202
    assert jwt.decode(token, app.secret_key, algorithm='HS256')["user"] == "user234134"

def test_jwt_refresh(client, db):
    now = datetime.datetime.utcnow()
    token = jwt.encode({"user": "12345", 
                        "exp": now},
                        app.secret_key).decode('utf-8')
    response = client.get('/users/jwt/refresh',
                headers={'Authorization': 'Bearer ' + token})

    refreshed_token = json.loads(response.data.decode('utf-8'))["jwt"].encode('utf-8')
    payload = jwt.decode(refreshed_token, app.secret_key)

    assert response.status_code == 200
    assert payload["user"] == "12345"
    assert payload["exp"] > int(now.timestamp())

def test_email_confirmation(client, db, user):
    s = URLSafeSerializer(app.secret_key)
    token = s.dumps(user.email)
    response = client.post('/users/email/confirmation', data={"token": token})

    assert response.status_code == 201
    user = query_user(user_id=user.id)
    assert user.email_confirmed
