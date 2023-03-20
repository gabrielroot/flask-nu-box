from flask import render_template
from flask_login import login_required, current_user
from projetoFlask.blueprints.webui.utils.OPTransactionEnum import TransactionOperation
from projetoFlask.blueprints.webui.repository.TransactionRepository import TransactionRepository

@login_required
def index():
    transactions = TransactionRepository.findMyActivesTransactions(current_user).limit(10)
    return render_template("dashboard.html", items=transactions, operation=TransactionOperation)