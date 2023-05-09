from click.testing import CliRunner

from nuBox.ext import commands
from nuBox.ext.database import User as UserModel
from nuBox.ext.database import db


def test_create_db(app):
    commands.create_db()
    assert len(db.engine.table_names()) >= 1
    assert 'users' in db.engine.table_names()


def test_drop_db(app):
    commands.drop_db()
    assert len(db.engine.table_names()) == 0


def test_create_user(app):
    commands.create_db()

    username = 'rand_user'

    runner = CliRunner()
    result = runner.invoke(
        app.cli.commands['add-user'], [
            '--username', username,
            '--password', '123'
        ]
    )

    user = UserModel.query.\
        filter_by(username=username).\
        first()

    assert user is not None
    assert user.username == username
    assert result.exit_code == 0
