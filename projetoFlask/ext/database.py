from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)

class Base(db.Model):
    __abstract__ = True
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)

class User(Base, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))

    boxes = db.relationship('Box', backref='user', lazy=True)

class Box(Base, SerializerMixin):
    __tablename__ = "boxes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    value = db.Column(db.Numeric())
    goal = db.Column(db.Numeric())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movimentations = db.relationship('Movimentation', backref='box', lazy=True)

class Movimentation(Base, SerializerMixin):
    __tablename__ = "movimentations"

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(140))
    value = db.Column(db.Numeric())
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    box_id = db.Column(db.Integer, db.ForeignKey('boxes.id'), nullable=False)


class Product(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    price = db.Column(db.Numeric())
    description = db.Column(db.Text)