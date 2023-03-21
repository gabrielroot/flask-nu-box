from datetime import datetime
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for
from projetoFlask.ext.database import Transaction as TransactionModel
from projetoFlask.blueprints.webui.services import flashMessagesService
from projetoFlask.blueprints.webui.repository.BoxRepository import BoxRepository
from projetoFlask.blueprints.webui.forms.TransactionForm import TransactionCreate
from projetoFlask.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from projetoFlask.blueprints.webui.repository.TransactionRepository import TransactionRepository

@login_required
def myTransactions():
    transactions = TransactionRepository.findMyActivesTransactions(current_user)
    return render_template("transactions/index.html", items=transactions, operation=TransactionOperation)

def newTransaction(box_id):
    form = TransactionCreate(request.form)
    box = BoxRepository.findOneActiveBox(id=box_id, current_user=current_user)

    if not box:
        flashMessagesService.addWarningMessage("Não encontramos sua caixinha.")
        return redirect(url_for('webui.myBoxes'))

    transaction = TransactionModel()
    balance = current_user.balance

    if request.method == 'POST':
        try:
            transaction.operation = form.operation.data
            transaction.description = form.description.data
            transaction.value = form.value.data
            transaction.date = datetime.utcnow()
            transaction.box = box

            if transaction.operation == TransactionOperation.DEPOSIT.name:
                if balance.total - transaction.value < 0:
                    flashMessagesService.addWarningMessage("Você não tem saldo suficiente para guardar este valor na caixinha.")
                    return render_template("transactions/depositWithdraw.html", form=form, box=box, transaction=transaction)
                
                box.value = box.value + transaction.value
                balance.total = balance.total - transaction.value
            elif transaction.operation == TransactionOperation.WITHDRAW.name:
                if box.value - transaction.value < 0:
                    flashMessagesService.addWarningMessage("Você tentou resgatar um valor maior do que o total guardado na caixinha.")
                    return render_template("transactions/depositWithdraw.html", form=form, box=box, transaction=transaction)
                
                box.value = box.value - transaction.value
                balance.total = balance.total + transaction.value

            balance.persist()
            transaction.persist()
            box.persist()

            flashMessagesService.addSuccessMessage("A caixinha foi movimentada com sucesso!")
            return redirect(url_for('webui.myTransactions', box_id=box.id))
        except:
            flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar movimentar a caixinha.")
          
    return render_template("transactions/depositWithdraw.html", form=form, box=box, transaction=transaction)

def newBalanceTransaction():
    form = TransactionCreate(request.form)
    balance = current_user.balance
    transaction = TransactionModel()

    if request.method == 'POST':
        try:
            transaction.operation = form.operation.data
            transaction.description = form.description.data
            transaction.value = form.value.data
            transaction.date = datetime.utcnow()
            transaction.balance_id = balance.id

            if transaction.operation == TransactionOperation.DEPOSIT.name:
                balance.total += transaction.value
            elif transaction.operation == TransactionOperation.WITHDRAW.name:
                if balance.total - transaction.value < 0:
                    flashMessagesService.addWarningMessage("Você tentou resgatar um valor maior do que o seu saldo total.")
                    return render_template("user/profile.html", form=form, transaction=transaction)
                
                balance.total -= transaction.value

            balance.persist()
            transaction.persist()

            flashMessagesService.addSuccessMessage("Saldo atualizado com sucesso!")
            return redirect(url_for('webui.profile'))
        except:
            flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar atualizar seu saldo.")
          
    return render_template("user/profile.html", form=form, transaction=transaction)