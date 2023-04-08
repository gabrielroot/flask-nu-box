from sqlalchemy_serializer import SerializerMixin

from nuBox.ext.database import Base, db


class Box(Base, SerializerMixin):
    __tablename__ = "boxes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    value = db.Column(db.Numeric(), default=0, nullable=False)
    goal = db.Column(db.Numeric(), default=0, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='box', lazy=True)
