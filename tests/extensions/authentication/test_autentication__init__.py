from flask import session


def test_should_load_logged_user(app, client, user):
    logged_user = app.login_manager.user_loader(user.id)

    assert logged_user is not None
    assert int(session["_user_id"]) > 0
