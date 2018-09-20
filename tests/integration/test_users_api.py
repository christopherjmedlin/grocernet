import pytest
import json
import jwt
import datetime

from veggienet.users import models
from veggienet.db import save_to_database

TEST_PASSWORD = "!Lov3MyPiano"


def query_user(user_id):
    """
    Helper for querying user from database with proper app context
    """
    return models.User.query.filter_by(id=user_id).first()


def query_user_by_username(username):
    return models.User.query.filter_by(username=username).first()


@pytest.fixture(scope="module")
def user(app):
    user = models.User("user234134", "!Lov3MyPiano",
                       "user234134@gmail.com", False)
    with app.app_context():
        save_to_database(user)
        # re-query user so it isn't expired and SQLAlchemy doesn't
        # attempt to refresh attributes
        return query_user(user.id)


def test_user_retrieve(client, db, user):
    response = client.get('/api/v1/users/' + str(user.id))
    data = response.data.decode('utf-8')

    assert user.username in data
    assert user.password not in data
    assert TEST_PASSWORD not in data


def test_login(client, db, user, app):
    response = client.post('/api/v1/users/jwt/retrieve',
                           data={"username": user.username,
                                 "password": TEST_PASSWORD})
    token = json.loads(response.data.decode('utf-8'))["jwt"].encode('utf-8')

    assert response.status_code == 202
    assert jwt.decode(token, app.secret_key, algorithm='HS256')[
        "user"] == user.username


def test_user_put(client, db, user):
    client.put('/api/v1/users/' + str(user.id),
               data={"username": "user3413",
                     "email": "user234134@gmail.com"})
    user = query_user(user.id)

    assert user.username == 'user3413'
    assert user.email == 'user234134@gmail.com'


def test_jwt_refresh(client, db, app):
    now = datetime.datetime.utcnow()
    token = jwt.encode({"user": "12345",
                        "exp": now},
                       app.secret_key).decode('utf-8')
    response = client.get('/api/v1/users/jwt/refresh',
                          headers={'Authorization': 'Bearer ' + token})

    refreshed_token = json.loads(
        response.data.decode('utf-8'))["jwt"].encode('utf-8')
    payload = jwt.decode(refreshed_token, app.secret_key)

    assert response.status_code == 200
    assert payload["user"] == "12345"
    assert payload["exp"] > int(now.timestamp())
