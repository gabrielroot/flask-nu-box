from flask import get_flashed_messages

from nuBox.ext.database import Box as BoxModel
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation


def test_should_flash_warning(client):
    response = client.post('/profile/deposit-withdraw',
                           data=dict(value=10000,
                                     description='testing',
                                     operation=TransactionOperation.WITHDRAW.name),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)

    assert len(messages) > 0
    assert messages[0][0] == 'warning'
    assert response.status_code == 200


def test_should_flash_success(client):
    response = client.post('/profile/deposit-withdraw',
                           data=dict(value=10000,
                                     description='testing',
                                     operation=TransactionOperation.DEPOSIT.name),
                           follow_redirects=True)

    messages = get_flashed_messages(with_categories=True)

    assert len(messages) > 0
    assert messages[0][0] == 'success'
    assert response.status_code == 200


def test_should_flash_danger(client, user):
    box = BoxModel(name='base_box_test', value=100, goal=100, user_id=user.id)
    box.persist()

    response = client.get(f"my-boxes/{box.id}/delete")
    messages = get_flashed_messages(with_categories=True)

    assert len(messages) > 0
    assert messages[0][0] == 'danger'
    assert response.status_code == 302
