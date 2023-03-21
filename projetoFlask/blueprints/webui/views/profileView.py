from flask import render_template, request
from flask_login import login_required
from projetoFlask.ext.database import Transaction as TransactionModel
from projetoFlask.blueprints.webui.forms.TransactionForm import TransactionCreate

@login_required
def profile():
    form = TransactionCreate(request.form)
    transaction = TransactionModel()

    return render_template("user/profile.html", form=form, transaction=transaction)