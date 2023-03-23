from datetime import datetime
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, abort
from nuBox.ext.database import Transaction as TransactionModel
from nuBox.blueprints.webui.services import flashMessagesService
from nuBox.blueprints.webui.repository.BoxRepository import BoxRepository
from nuBox.blueprints.webui.forms.TransactionForm import TransactionCreate
from nuBox.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from nuBox.blueprints.webui.repository.TransactionRepository import TransactionRepository

@login_required
def myTransactions():
    page = request.args.get('page', 1, type=int)
    pagination = TransactionRepository.findMyActivesTransactions(current_user).paginate(page=page, per_page=10, error_out=False)
    return render_template("transactions/index.html", pagination=pagination, operation=TransactionOperation)

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
            return redirect(url_for('webui.myTransactions'))
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