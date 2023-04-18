import pytest

from nuBox.app import create_app
from nuBox.ext.database import db
from nuBox.ext.authentication.views.authView import create_user


@pytest.fixture(scope="module")
def app():
    app = create_app(env='testing')
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture(scope="module")
def user(app):
    with app.app_context():
        user = create_user(username="my_user", password='plain_password')
        yield user
