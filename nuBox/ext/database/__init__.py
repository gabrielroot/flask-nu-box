from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


from .Base import Base
from .User import User
from .Balance import Balance
from .Transaction import Transaction
from .Box import Box

__all__ = ('User', 'Box', 'Transaction', 'Balance', 'Base')
