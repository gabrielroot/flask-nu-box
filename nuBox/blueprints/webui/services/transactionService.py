from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation


def makeDepositOrWithdraw(transaction, box, balance):
    if transaction.operation == TransactionOperation.DEPOSIT.name:
        if balance.total - transaction.value < 0:
            return "Você não tem saldo suficiente para guardar este valor na caixinha."

        box.value += transaction.value
        balance.total -= transaction.value
    elif transaction.operation == TransactionOperation.WITHDRAW.name:
        if box.value - transaction.value < 0:
            return "Você tentou resgatar um valor maior do que o saldo da caixinha."

        box.value -= transaction.value
        balance.total += transaction.value

    balance.persist()
    transaction.persist()
    box.persist()


def makeDepositOrWithdrawAtBalance(transaction, balance):
    if transaction.operation == TransactionOperation.DEPOSIT.name:
        balance.total += transaction.value
    elif transaction.operation == TransactionOperation.WITHDRAW.name:
        if balance.total - transaction.value < 0:
            return "Você tentou resgatar um valor maior do que o seu saldo total."

        balance.total -= transaction.value

    balance.persist()
    transaction.persist()
