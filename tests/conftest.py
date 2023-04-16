import pytest
from nuBox.app import create_app
from nuBox.ext.database import db


@pytest.fixture(scope="module")
def app():
    app = create_app(env='testing')
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
