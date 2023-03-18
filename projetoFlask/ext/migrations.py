from flask_migrate import Migrate
from projetoFlask.ext.database import db


def init_app(app):
    Migrate(app, db)