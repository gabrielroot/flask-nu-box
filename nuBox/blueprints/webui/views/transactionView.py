from datetime import datetime

from flask import request, url_for, redirect, render_template
from flask_login import current_user, login_required

from nuBox.ext.database import Transaction as TransactionModel
from nuBox.blueprints.webui.services import transactionService, flashMessagesService
from nuBox.blueprints.webui.forms.TransactionForm import TransactionCreate
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from nuBox.blueprints.webui.repository.BoxRepository import BoxRepository
from nuBox.blueprints.webui.repository.TransactionRepository import TransactionRepository


@login_required
def myTransactions():
    page = request.args.get('page', 1, type=int)
    pagination = TransactionRepository.findMyActivesTransactions(current_user).\
        paginate(page=page, per_page=10, error_out=False)
    return render_template("transactions/index.html", pagination=pagination, operation=TransactionOperation)


@login_required
def newTransaction(box_id):
    form = TransactionCreate(request.form)
    box = BoxRepository.findOneActiveBox(id=box_id, current_user=current_user)

    if not box:
        flashMessagesService.addWarningMessage("Não encontramos sua caixinha.")
        return redirect(url_for('webui.myBoxes'))

    transaction = TransactionModel()
    balance = current_user.balance

    if form.validate_on_submit():
        try:
            transaction.operation = form.operation.data
            transaction.description = form.description.data
            transaction.value = form.value.data
            transaction.date = datetime.utcnow()
            transaction.box = box

            errorMessage = transactionService.makeDepositOrWithdraw(transaction=transaction, box=box, balance=balance)

            if errorMessage:
                flashMessagesService.addWarningMessage(errorMessage)
                return render_template("transactions/depositWithdraw.html", form=form, box=box, transaction=transaction)

            flashMessagesService.addSuccessMessage("A caixinha foi movimentada com sucesso!")
            return redirect(url_for('webui.myTransactions'))
        except Exception:
            flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar movimentar a caixinha.")

    return render_template("transactions/depositWithdraw.html", form=form, box=box, transaction=transaction)


@login_required
def newBalanceTransaction():
    form = TransactionCreate(request.form)
    balance = current_user.balance
    transaction = TransactionModel()

    if form.validate_on_submit():
        try:
            transaction.operation = form.operation.data
            transaction.description = form.description.data
            transaction.value = form.value.data
            transaction.date = datetime.utcnow()
            transaction.balance_id = balance.id

            errorMessage = transactionService.makeDepositOrWithdrawAtBalance(transaction=transaction, balance=balance)

            if errorMessage:
                flashMessagesService.addWarningMessage(errorMessage)
                return render_template("user/profile.html", form=form, transaction=transaction)

            flashMessagesService.addSuccessMessage("Saldo atualizado com sucesso!")
            return redirect(url_for('webui.profile'))
        except Exception:
            flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar atualizar seu saldo.")

    return render_template("user/profile.html", form=form, transaction=transaction)
