from datetime import datetime

from nuBox.ext.database import db


class Base(db.Model):
    __abstract__ = True

    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime)
    deletedAt = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def persist(self, flush=False):
        self.updatedAt = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

        if flush:
            db.session.refresh(self)
            db.session.flush()

        return self

    def remove(self, flush=False):
        self.deleted = True
        self.deletedAt = datetime.utcnow()

        db.session.add(self)
        db.session.commit()

        if flush:
            db.session.refresh(self)
            db.session.flush()

        return self
