from datetime import datetime
from flask import render_template, request, redirect, url_for
from projetoFlask.blueprints.webui.forms.TransactionForm import TransactionCreate
from flask_login import login_required, current_user
from projetoFlask.ext.database import Box as BoxModel, Transaction as TransactionModel, Balance as BalanceModel
from projetoFlask.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from projetoFlask.ext.database import db
from projetoFlask.blueprints.webui.services import flashMessagesService


@login_required
def myTransactions():
    transactions = TransactionModel.query.filter_by(deleted=False).order_by(TransactionModel.createdAt.desc())
    return render_template("transactions/index.html", items=transactions, operation=TransactionOperation)

def newTransaction(box_id):
    form = TransactionCreate(request.form)
    box = db.get_or_404(BoxModel, box_id)
    transaction = TransactionModel()
    balance = BalanceModel.query.filter_by(user=current_user).first()

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