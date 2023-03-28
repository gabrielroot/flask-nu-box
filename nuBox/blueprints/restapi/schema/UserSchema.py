from nuBox.ext.marshmallow import ma
from nuBox.ext.database import User as UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        include_fk = True

    id = ma.auto_field()
    username = ma.auto_field()
    createdAt = ma.auto_field()
    deletedAt = ma.auto_field()
    deleted = ma.auto_field()
    updatedAt = ma.auto_field()
