<p align="center">
    <a href="https://grocernet.christophermedlin.me">
        <img src="https://raw.githubusercontent.com/christopherjmedlin/grocernet/master/logo.png"/>
    </a>
</p>

Grocernet is a business rating website with a focus on finding high quality groceries.

#### How do I run this abomination?

To run Grocernet, you should first create a [virtual environment](https://virtualenv.pypa.io/en/stable/)
and install the requirements

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# if you plan to run the tests
pip install -r dev-requirements.txt
```

Next you should specify some configuration options in `instance/config.py`:

```
SQLALCHEMY_DATABASE_URI = <your database URI>
TEST_DATABASE_URI = <the database to be used when running tests>

SECRET_KEY = <your secret key>
ENVIRONMENT = 'dev'

# flask_mail stuff
MAIL_DEFAULT_SENDER = <mail sender>
MAIL_HOST = <host of mail server>
MAIL_PORT = <port of mail server>

# mapbox stuff
MAPBOX_ACCESS_TOKEN = <mapbox token to be used in backend geocoding>
MAPBOX_PUBLIC_ACCESS_TOKEN = <mapbox token to be used in frontend map>
```
To run the app:

`PYTHONPATH=. FLASK_APP=grocernet.wsgi venv/bin/flask run`

#### How do I run the tests?

To run tests:

`PYTHONPATH=. venv/bin/py.test tests/`

You may also skip tests that require Mapbox services by skipping the mapbox_required marker:

`PYTHONPATH=. venv/bin/py.test tests/ -m "not mapbox_required"`

To run Selenium tests (assuming you have the Chrome webdriver installed):

```
# first create a test user
PYTHONPATH=. FLASK_APP=grocernet.wsgi venv/bin/flask createuser

PYTHONPATH=. venv/bin/py.test selenium-tests/ --testuser <username> --testpassword <password>
```
