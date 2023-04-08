from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from nuBox.ext.database import Base, db


class User(Base, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), nullable=False)
    password = db.Column(db.String(512), nullable=False)

    boxes = db.relationship('Box', backref='user', lazy=True)
    balance = db.relationship('Balance', backref='user', uselist=False)
