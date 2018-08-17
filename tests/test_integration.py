import pytest

from veggienet import create_app
from veggienet import models

from werkzeug.security import check_password_hash

app = create_app(testing=True)

@pytest.fixture(scope="module")
def client():
    return app.test_client()

@pytest.fixture(scope="function")
def db():
    with app.app_context():
        models.db.drop_all()
        models.db.create_all()
        return models.db

def test_user_retrieve(client, db):
    response = None
    user = models.User("user234134", "!Lov3MyPiano",
                       "user234134@gmail.com", False)

    with app.app_context():
        models.save_to_database(user)
        response = client.get('/users/' + str(user.id))
    
    assert b'"user234134"' in response.data

def test_user_put(client, db):
    response = None
    user = models.User("user234134", "SterlingGmail20.15",
                       "user234134@gmail.com", False)
    
    with app.app_context():
        models.save_to_database(user)
        response = client.put('/users/' + str(user.id),
                data={"username": "user23413", "email": "user234134@gmail.com"})
        user = models.User.query.filter_by(id=user.id).first()

    assert user.username == 'user23413'
        
def test_valid_user_post(client, db):
    response = None
    user = None

    with app.app_context():
        response = client.post('/users/', data={"username": "user24315",
                            "email": "user24315@gmail.com", "password": "s3cur3P@$$w0rd"})
        user = models.User.query.filter_by(username="user24315").first()

    assert check_password_hash(user.password, "s3cur3P@$$w0rd")
    assert not user.admin

@pytest.mark.parametrize("username,password,email", [
    (None, None, None),
    ("user34737", "278374", "user34737@gmail.com"),
    ("Mr. Smith", "s3cur3P@$$w0rd", "mrsmith@gmail.com"),
    ("user73758", "s3cur3P@$$w0rd", "user73758@gmailcom")
])
def test_invalid_user_post(client, db, username, password, email):
    response = None

    with app.app_context():
        response = client.post('/users/', data={"username": username,
                            "email": email, "password": password})
    assert response.status_code == 400
    assert b"Invalid" in response.data or b"Missing" in response.data
