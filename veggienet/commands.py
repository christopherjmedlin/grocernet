from . import db, app
from getpass import getpass
from .models import User

@app.cli.command('initdb')
def initdb():
    """Initializes the database."""
    db.create_all()
    print('Initialized the database.')

@app.cli.command('createuser')
def createuser():
    username = input("Username: ")
    password = getpass("Password: ")
    email = input("Email: ")
    admin = input("Admin? y or n: ").lower()

    if admin == 'y':
        admin = True
    else:
        admin = False

    user = User(username, email, password, admin)
    db.session.add(user)
    db.session.commit()
