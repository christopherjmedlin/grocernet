from getpass import getpass
from veggienet.users.models import User
from veggienet.db import db
from flask.cli import with_appcontext
import click


@click.command('initdb')
@with_appcontext
def initdb():
    """Initializes the database."""
    db.create_all()
    print('Initialized the database.')


@click.command('createuser')
@with_appcontext
def createuser():
    username = input("Username: ")
    password = getpass("Password: ")
    email = input("Email: ")
    admin = input("Admin? y or n: ").lower()

    if admin == 'y':
        admin = True
    else:
        admin = False

    user = User(username, password, email, admin)
    user.activated = True
    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()
