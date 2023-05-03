from flask import session, get_flashed_messages

from nuBox.ext.database import User as UserModel


def test_should_login_succesfully(client):
    session['_user_id'] = None
    response = client.post('/auth/login',
                           data=dict(username='my_user', password='plain_password'),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)

    assert len(messages) > 0
    assert messages[0][0] == 'success'
    assert response.status_code == 200
    assert '_user_id' in session


def test_should_do_not_login(client):
    response = client.post('/auth/login',
                           data=dict(username='404_user', password='plain_password'),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)

    assert len(messages) > 0
    assert messages[0][0] == 'danger'
    assert response.status_code == 200


def test_should_create_user_succesfully(client):
    response = client.post('/auth/signup',
                           data=dict(username='new_user', password='plain_password'),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'success'

    created_user = UserModel.query.filter_by(
        username='new_user'
    ).first()
    assert created_user is not None
    assert created_user.username == 'new_user'

    assert response.status_code == 200


def test_should_raise_fail_username_constraint(client):
    response = client.post('/auth/signup',
                           data=dict(username='new_user',
                                     password='plain_password'),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)
    assert len(messages) > 0
    assert messages[0][0] == 'warning'

    unique_created_user = UserModel.query.filter_by(
        username='new_user'
    ).all()
    assert unique_created_user is not None
    assert len(unique_created_user) == 1

    assert response.status_code == 200


def test_should_logout_succesfully(client):
    response = client.get('/auth/logout',
                          follow_redirects=True)

    assert response.status_code == 200
    assert '_user_id' not in session or\
           session['_user_id'] > 0

    client.post('/auth/login',
                data=dict(username='my_user',
                          password='plain_password'))
