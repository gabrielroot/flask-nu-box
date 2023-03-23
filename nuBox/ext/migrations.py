from flask_migrate import Migrate
from nuBox.ext.database import db


def init_app(app):
    Migrate(app, db)