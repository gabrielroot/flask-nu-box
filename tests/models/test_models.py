from nuBox.ext.database import Box as BoxModel, User as UserModel
from nuBox.ext.authentication.views.authView import create_user


def test_create_first_user(app):
    plain_password = 'pass123'
    user = create_user(username="test_user", password=plain_password)

    assert user.id is not None
    assert user.password != plain_password


def test_create_box(app):
    first_user = UserModel.query.one()
    box = BoxModel(name='boxname', value=0, goal=100, user_id=first_user.id)
    box.persist()

    assert box.id is not None
