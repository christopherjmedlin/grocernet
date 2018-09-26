import pytest
from grocernet import create_app
from grocernet.db import db as sql


@pytest.fixture(scope="module")
def app():
    app = create_app(testing=True)
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def db(app):
    sql.drop_all()
    sql.create_all()
    return sql
