from enum import Enum
from datetime import datetime

from nuBox.ext.database import Box as BoxModel
from nuBox.ext.database import Transaction as TransactionModel
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from nuBox.blueprints.webui.services.transactionService import makeDepositOrWithdraw
from nuBox.blueprints.webui.services.transactionService import makeDepositOrWithdrawAtBalance


class TransactionType(Enum):
    BOX = 'box'
    BALANCE = 'balance'


def makeTransaction(transaction_type, operation, value, target):
    transaction = TransactionModel(value=value, date=datetime.utcnow(), operation=operation)

    if transaction_type == TransactionType.BOX.name:
        transaction.box_id = target.id
    elif transaction_type == TransactionType.BALANCE.name:
        transaction.balance_id = target.id

    return transaction


def test_deposit_withdraw_at_box(user):
    user.balance.total = 200
    user.balance.persist()

    box = BoxModel(name='box_transaction_test', value=0, goal=100, user_id=user.id)
    box.persist()

    transaction = makeTransaction(TransactionType.BOX.name, TransactionOperation.DEPOSIT.name, 100, box)
    assert None is makeDepositOrWithdraw(box=box, balance=user.balance, transaction=transaction)

    transaction = makeTransaction(TransactionType.BOX.name, TransactionOperation.WITHDRAW.name, 100, box)
    assert None is makeDepositOrWithdraw(box=box, balance=user.balance, transaction=transaction)

    transaction = makeTransaction(TransactionType.BOX.name, TransactionOperation.DEPOSIT.name, 300, box)
    assert makeDepositOrWithdraw(box=box, balance=user.balance, transaction=transaction) is not None

    transaction = makeTransaction(TransactionType.BOX.name, TransactionOperation.WITHDRAW.name, 200, box)
    assert makeDepositOrWithdraw(box=box, balance=user.balance, transaction=transaction) is not None


def test_deposit_withdraw_at_balance(user):
    balance = user.balance
    balance.total = 0
    balance.persist()

    transaction = makeTransaction(TransactionType.BALANCE.name, TransactionOperation.DEPOSIT.name, 100, balance)
    assert None is makeDepositOrWithdrawAtBalance(balance=user.balance, transaction=transaction)

    transaction = makeTransaction(TransactionType.BALANCE.name, TransactionOperation.WITHDRAW.name, 100, balance)
    assert None is makeDepositOrWithdrawAtBalance(balance=user.balance, transaction=transaction)

    transaction = makeTransaction(TransactionType.BALANCE.name, TransactionOperation.WITHDRAW.name, 200, balance)
    assert makeDepositOrWithdrawAtBalance(balance=user.balance, transaction=transaction) is None
