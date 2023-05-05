from flask import get_flashed_messages
from flask_login import current_user

from nuBox.ext.database import Box as BoxModel


def test_should_render_view(client):
    response = client.get('/my-boxes', follow_redirects=True)
    assert response.status_code == 200


def test_should_create_a_box(client):
    response = client.post('/my-boxes/new',
                           data=dict(name='new_box', goal=100),
                           follow_redirects=True)

    box_created = BoxModel.query.filter_by(name='new_box', goal=100).first()

    assert response.status_code == 200
    assert box_created is not None
    assert box_created.user_id == current_user.id


def test_should_fail_when_is_invalid(app, client):
    response = client.get('/my-boxes/new')
    assert response.status_code == 200

    response = client.post('/my-boxes/new',
                           data=dict(name='', goal=-100),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'danger'

    box_not_created = BoxModel.query.filter_by(name='new_box_fail', goal=100).\
        first()

    assert response.status_code == 200
    assert box_not_created is None


def test_should_edit_a_box(client):
    box = BoxModel.query.first()
    response = client.get(f"/my-boxes/{box.id}/edit")
    assert response.status_code == 200

    response = client.post(f"/my-boxes/{box.id}/edit",
                           data=dict(name='valid_box', goal=120),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'success'

    BoxModel.query.filter_by(name='valid_box', goal=120).\
        first()

    assert response.status_code == 200


def test_should_fail_when_edit_is_invalid(app, client):
    client.get("/my-boxes/404/edit", follow_redirects=True)
    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'warning'

    box = BoxModel.query.first()
    client.post(f"/my-boxes/{box.id}/edit",
                data=dict(name='', goal=-110),
                follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'danger'

    box_not_edited = BoxModel.query.filter_by(goal=-110).\
        first()

    assert box_not_edited is None


def test_should_fail_on_delete(client):
    box = BoxModel.query.first()
    box.value = 100
    box.persist()

    client.get(f"/my-boxes/{box.id}/delete", follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'danger'

    client.get("/my-boxes/404/delete", follow_redirects=True)
    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'warning'


def test_should_successfully_delete(client):
    box = BoxModel.query.first()
    box.value = 0
    box.persist()

    client.get(f"/my-boxes/{box.id}/delete", follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'success'
