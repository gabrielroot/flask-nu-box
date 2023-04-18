from datetime import datetime

from nuBox.ext.database import Box as BoxModel
from nuBox.ext.database import Transaction as TransactionModel
from nuBox.ext.authentication.views.authView import create_user
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation


def test_create_user(app):
    plain_password = 'pass123'
    user = create_user(username="test_user", password=plain_password)

    assert user.id is not None
    assert user.balance.total == 0
    assert user.password != plain_password


def test_base_model(user):
    box = BoxModel(name='base_box_test', value=0, goal=100, user_id=user.id)
    box.persist()

    now = datetime.utcnow()
    assert type(box.createdAt) == type(now)

    box.persist(True)
    assert box.updatedAt > box.createdAt

    box.remove(True)
    assert box.deletedAt > box.createdAt
    assert box.deleted is not None


def test_create_box(user):
    box = BoxModel(name='boxname', value=0, goal=100, user_id=user.id)
    box.persist()

    assert box.id is not None


def test_create_transaction(user):
    first_box = BoxModel.query.first()

    transaction = TransactionModel(
        operation=TransactionOperation.DEPOSIT.name,
        value=100,
        date=datetime.utcnow()
    )

    transactionBalance = transaction
    transactionBalance.balance_id = user.balance.id
    transactionBalance.persist()

    transactionBox = transaction
    transactionBox.box_id = first_box.id
    transactionBox.persist()

    transaction.persist()

    assert transaction.id is not None
    assert transactionBalance.id is not None
    assert transactionBox.id is not None
