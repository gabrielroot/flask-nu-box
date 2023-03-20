from flask import render_template
from flask_login import login_required
from projetoFlask.ext.database import Transaction as TransactionModel
from projetoFlask.blueprints.webui.utils.OPTransactionEnum import TransactionOperation

@login_required
def index():
    transactions = TransactionModel.query.filter_by(deleted=False).order_by(TransactionModel.createdAt.desc()).limit(10)
    return render_template("dashboard.html", items=transactions, operation=TransactionOperation)