from nuBox.ext.database import db, Base
from sqlalchemy_serializer import SerializerMixin


class Balance(Base, SerializerMixin):
    __tablename__ = "balances"

    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Numeric(), default=0, nullable=False)

    transactions = db.relationship('Transaction', backref='balance', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
