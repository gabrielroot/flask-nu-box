from datetime import datetime

from sqlalchemy_serializer import SerializerMixin

from nuBox.ext.database import Base, db


class Transaction(Base, SerializerMixin):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(140), nullable=False)
    value = db.Column(db.Numeric(), default=0, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    box_id = db.Column(db.Integer, db.ForeignKey('boxes.id'))
    balance_id = db.Column(db.Integer, db.ForeignKey('balances.id'), nullable=True)
