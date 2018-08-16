import pytest

from veggienet import create_app
from veggienet import models

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

def test_valid_user_put(client, db):
    response = None
    user = models.User("user234134", "SterlingGmail20.15",
                       "user234134@gmail.com", False)
    
    with app.app_context():
        models.save_to_database(user)
        response = client.put('/users/' + str(user.id),
                data="{'user': 'user23413', 'email': 'user234134@gmail.com'}")

        

                       

